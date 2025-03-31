import os
import subprocess
from typing import Literal

import gradio as gr
import openai
import requests
from agentdojo.agent_pipeline import (
    AgentPipeline,
    InitQuery,
    OpenAILLM,
    PromptInjectionDetector,
    SystemMessage,
    ToolsExecutionLoop,
    ToolsExecutor,
)
from agentdojo.ast_utils import create_python_function_from_tool_call
from agentdojo.functions_runtime import FunctionsRuntime
from agentdojo.logging import OutputLogger
from agentdojo.types import ChatMessage
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from dtx_prompt_guard_client.guard import DtxPromptGuardClient
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DTXPROMPT_GUARD_SVC_URL = os.getenv("DTXPROMPT_GUARD_SVC_URL", "http://localhost:8000/")

if not DTXPROMPT_GUARD_SVC_URL:
    raise ValueError("DTXPROMPT_GUARD_SVC_URL is missing")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")


class DtxBasedInjectionDetection(PromptInjectionDetector):
    """Uses DtxPromptGuardClient to detect prompt injections.

    Args:
        base_url: The base URL of the DtxPromptGuard service.
        threshold: The threshold for the model's prediction to be considered a prompt injection.
        mode: The mode in which the detector should operate. It can be 'message' or 'full_conversation'.
        raise_on_injection: Whether to raise an exception if a prompt injection is detected.
    """
    def __init__(
        self,
        base_url: str,
        threshold: float = 0.8,
        mode: Literal["message", "full_conversation"] = "message",
        raise_on_injection: bool = False,
    ) -> None:
        super().__init__(mode=mode, raise_on_injection=raise_on_injection)
        self.client = DtxPromptGuardClient(base_url=base_url, threshold=threshold)
        self.threshold = threshold

    def detect(self, tool_output: str) -> tuple[bool, float]:
        is_injection = self.client.contain_prompt_injection(tool_output)
        safety_score = 1.0 if not is_injection else 0.0
        return is_injection, safety_score

    def jailbreak(self, query: str) -> tuple[bool, float]:
        is_injection = self.client.contain_jailbreak(query)
        safety_score = 1.0 if not is_injection else 0.0
        return is_injection, safety_score


class DetectorFactory:
    def __init__(self, base_url, threshold=0.8):
        self.PROMPT_INJECTION_DETECTiON = None
        self.base_url = base_url
        self.threshold = threshold

    def get_prompt_injection_detection(
        self, enable_pidetection: bool = False, raise_on_injection: bool = True
    ):
        if enable_pidetection and not self.PROMPT_INJECTION_DETECTiON:
            self.PROMPT_INJECTION_DETECTiON = DtxBasedInjectionDetection(
                base_url=self.base_url,
                threshold=self.threshold,
                raise_on_injection=raise_on_injection,
            )
        return self.PROMPT_INJECTION_DETECTiON


class GradioOutputLogger(OutputLogger):
    def __init__(self):
        super().__init__(logdir=None, live=None)
        self.messages = []

    def log(self, messages: list[ChatMessage], **kwargs):
        """Logs system messages, user input, tool calls, and responses as assistant messages, avoiding duplicates."""
        messages = messages[len(self.messages):]  # Avoid logging already stored messages
        for message in messages:
            role = message.get("role", "unknown")
            content = (
                str(message.get("content", ""))
                if message.get("content") is not None
                else ""
            )
            formatted_message = {}
            if role == "assistant":
                tool_calls = message.get("tool_calls", [])
                tool_calls_content = ""
                if tool_calls:
                    tool_calls_content = "\n------------\n🔧 ### Tool Calls:\n"
                    for tool_call in tool_calls:
                        try:
                            python_function = create_python_function_from_tool_call(tool_call)
                            tool_calls_content += f"  - {python_function}\n"
                        except Exception as e:
                            tool_calls_content += f"  - Error formatting function: {str(e)}\n"
                formatted_message = {
                    "role": "assistant",
                    "content": f"### 🤖 Assistant:\n {content}{tool_calls_content}",
                }
            elif role == "tool":
                formatted_message = {
                    "role": "assistant",
                    "content": f"🔧 Tool Execution: {content}",
                }
            if formatted_message and not any(
                msg["role"] == formatted_message["role"] and msg["content"] == formatted_message["content"]
                for msg in self.messages
            ):
                self.messages.append(formatted_message)

    def get_messages(self):
        """Returns all formatted messages that follow Gradio's 'assistant' and 'user' roles."""
        return self.messages


class BaseAgent:
    def _format_articles(self, articles):
        """Formats a list of articles into a user-friendly string output.

        Args:
            articles (list of dict): List of articles with 'title', 'href', and 'body' keys.
        Returns:
            str: Formatted string displaying articles in a readable format.
        """
        formatted_output = []
        for index, article in enumerate(articles, start=1):
            title = article.get("title", "No Title")
            link = article.get("href", "#")
            body = article.get("body", "No description available.")
            formatted_output.append(
                f"📰 **{index}. {title}**\n🔗 [Read more]({link})\n📌 {body}\n"
            )
        return "\n".join(formatted_output)

    def _fetch_webpage_content(self, url: str) -> str:
        """Fetches a web page and extracts its main text content.
        Args:
            url (str): The URL of the web page.
        Returns:
            str: Extracted readable content from the web page.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            extracted_text = "\n".join([p.get_text() for p in paragraphs])
            return extracted_text if extracted_text else "No readable content found on this page."
        except requests.exceptions.RequestException as e:
            return f"Error fetching webpage: {str(e)}"


class EmailAgent(BaseAgent):
    NAME = "Email Agent"
    SYSTEM_MESSAGE = "You are a helpful assistant who always take safe actions"

    def __init__(self, pi_detector, system_message=None):
        if system_message is None:
            system_message = self.SYSTEM_MESSAGE
        self.llm = OpenAILLM(openai.OpenAI(), "gpt-4o-2024-05-13")
        tools = [ToolsExecutor()]
        if pi_detector:
            tools.append(pi_detector)
        tools.append(self.llm)
        self.tools_loop = ToolsExecutionLoop(tools)
        self.pipeline = AgentPipeline(
            [
                SystemMessage(system_message),
                InitQuery(),
                self.llm,
                self.tools_loop,
            ]
        )
        self.runtime = FunctionsRuntime([])
        self.logger = GradioOutputLogger()
        self._register_functions()

    def _register_functions(self):
        @self.runtime.register_function
        def send_email(address: str, subject: str, body: str):
            """Sends an email.
            :param address: The recipient email address.
            :param subject: The subject of the email.
            :param body: The body of the email.
            :return: Confirmation message.
            """
            return f"Email sent successfully to {address} with body: {body}"

        @self.runtime.register_function
        def web_search(query: str):
            """Perform web search for new information using the DuckDuckGo search engine.
            :param query: The search query to perform.
            :return: Formatted string containing search results.
            """
            return self._format_articles(DDGS().text(query, max_results=5))

    def execute(self, prompt):
        with self.logger:
            self.pipeline.query(prompt, self.runtime)
        return self.logger.get_messages()


class CommandExecuteAgent(BaseAgent):
    NAME = "Safe Command Execution"
    SYSTEM_MESSAGE = "You are a command execution assistant who always take safe actions and run safe commands"

    def __init__(self, pi_detector, system_message=None):
        if system_message is None:
            system_message = self.SYSTEM_MESSAGE
        self.llm = OpenAILLM(openai.OpenAI(), "gpt-4o-2024-05-13")
        tools = []
        if pi_detector:
            tools.append(pi_detector)
        tools.append(ToolsExecutor())
        if pi_detector:
            tools.append(pi_detector)
        tools.append(self.llm)
        self.tools_loop = ToolsExecutionLoop(tools)
        self.pipeline = AgentPipeline(
            [
                SystemMessage(system_message),
                InitQuery(),
                self.llm,
                self.tools_loop,
            ]
        )
        self.runtime = FunctionsRuntime([])
        self.logger = GradioOutputLogger()
        self._register_functions()

    def _register_functions(self):
        @self.runtime.register_function
        def web_search(query: str):
            """Perform web search for new information using the DuckDuckGo search engine.
            :param query: The search query to perform.
            :return: A formatted string containing the search results.
            """
            return self._format_articles(DDGS().text(query, max_results=5))

        @self.runtime.register_function
        def fetch_webpage(url: str):
            """Fetches and parses the text content of a web page from a given URL.
            :param url: The URL of the web page to fetch.
            :return: A string containing the main content of the page.
            """
            return self._fetch_webpage_content(url)

        @self.runtime.register_function
        def execute_bash(command: str):
            """Executes a bash command.
            :param command: The shell command to execute.
            :return: The output of the command or an error message.
            """
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout.strip() if result.stdout else result.stderr.strip()
                return f"Command Output: {output}"
            except Exception as e:
                return f"Error executing command: {str(e)}"

    def execute(self, prompt):
        with self.logger:
            self.pipeline.query(prompt, self.runtime)
        return self.logger.get_messages()


DEFAULT_AGENT = CommandExecuteAgent
detector_factory = DetectorFactory(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)


def get_default_system_message(agent_name):
    if agent_name == EmailAgent.NAME:
        return EmailAgent.SYSTEM_MESSAGE
    elif agent_name == CommandExecuteAgent.NAME:
        return CommandExecuteAgent.SYSTEM_MESSAGE
    else:
        return ""


def update_system_message(agent_name):
    """Update the system message based on agent selection."""
    return get_default_system_message(agent_name)


def chat_response(history, user_input, agent, system_message, enable_security, jailbreak_detection, enable_pidetection):
    formatted_history = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    formatted_history.append({"role": "user", "content": user_input})
    
    # First: Check prompt injection detection if enabled (using only the detect method)
    if enable_pidetection:
        detector = detector_factory.get_prompt_injection_detection(enable_pidetection=True, raise_on_injection=False)
        if detector:
            is_injection, _ = detector.detect(user_input)
            if is_injection:
                formatted_history.append({"role": "assistant", "content": "⚠️ Malicious input detected (Prompt Injection). Command aborted."})
                return formatted_history, ""
    
    # Then: Check jailbreak detection if security is enabled and the checkbox is checked
    if enable_security and jailbreak_detection:
        detector = detector_factory.get_prompt_injection_detection(enable_pidetection=True, raise_on_injection=False)
        if detector:
            is_injection, _ = detector.jailbreak(user_input)
            if is_injection:
                formatted_history.append({"role": "assistant", "content": "⚠️ Malicious input detected (Jailbreak). Command aborted."})
                return formatted_history, ""
    
    # If no malicious input detected, proceed with the chosen agent.
    if agent == EmailAgent.NAME:
        agent_instance = EmailAgent(detector_factory.get_prompt_injection_detection(enable_pidetection=False), system_message)
    elif agent == CommandExecuteAgent.NAME:
        agent_instance = CommandExecuteAgent(detector_factory.get_prompt_injection_detection(enable_pidetection=False), system_message)
    else:
        formatted_history.append({"role": "assistant", "content": "Agent Not Found"})
        return formatted_history, ""
    
    if agent_instance:
        response = agent_instance.execute(user_input)
        formatted_history.extend(response)
    
    return formatted_history, ""


def clear_chat():
    return [], ""


with gr.Blocks() as demo:
    # Title and Description
    gr.Markdown(
        """
        # Demo Tool Agents
        **Configure your agent and chat using advanced security options.**
        """
    )
    
    with gr.Accordion("Configure", open=True):
        # Editable textbox for the system prompt using updated function
        system_message_box = gr.Textbox(
            label="System Message",
            value=get_default_system_message(DEFAULT_AGENT.NAME),
            lines=4,
            placeholder="Enter a custom system prompt here..."
        )

        agent_selection = gr.Radio(
            [EmailAgent.NAME, CommandExecuteAgent.NAME],
            label="Choose an Agent",
            value=DEFAULT_AGENT.NAME,
        )

        agent_selection.change(
            update_system_message,
            inputs=[agent_selection],
            outputs=[system_message_box],
        )

        # Button to reset system prompt to the agent default.
        reset_prompt_btn = gr.Button("Reset System Prompt")
        reset_prompt_btn.click(
            update_system_message,
            inputs=[agent_selection],
            outputs=[system_message_box],
        )

        # Advanced Security Options section with three checkboxes
        with gr.Accordion("Advanced Security Options", open=True):
            enable_security = gr.Checkbox(label="Enable Security Checks", value=False)
            jailbreak_checkbox = gr.Checkbox(label="Check Malicious User Input (Jailbreak Detection)", value=False, interactive=False)
            # Callback to toggle the jailbreak checkbox
            def toggle_jailbreak(enable):
                if enable:
                    return gr.update(interactive=True, value=True)
                else:
                    return gr.update(interactive=False, value=False)
            enable_security.change(toggle_jailbreak, inputs=[enable_security], outputs=[jailbreak_checkbox])
            
            # Define and initialize the prompt injection detection checkbox as disabled
            def toggle_pidetection(enable):
                if enable:
                    return gr.update(interactive=True)
                else:
                    return gr.update(interactive=False, value=False)
            enable_pidetection = gr.Checkbox(label="Check Malicious Context Input (Prompt Injection Detection)", value=False, interactive=False)
            enable_security.change(toggle_pidetection, inputs=[enable_security], outputs=[enable_pidetection])

    chat_history = gr.Chatbot(label="Chat Window", type="messages")
    user_input = gr.Textbox(label="Enter your message")

    # Bind submit events to the updated callback signature including all security options.
    user_input.submit(
        chat_response,
        inputs=[
            chat_history,
            user_input,
            agent_selection,
            system_message_box,
            enable_security,
            jailbreak_checkbox,
            enable_pidetection,
        ],
        outputs=[chat_history, user_input],
    )

    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")

    submit_btn.click(
        chat_response,
        inputs=[
            chat_history,
            user_input,
            agent_selection,
            system_message_box,
            enable_security,
            jailbreak_checkbox,
            enable_pidetection,
        ],
        outputs=[chat_history, user_input],
    )
    clear_btn.click(clear_chat, inputs=[], outputs=[chat_history, user_input])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")













# # Previous code to check logic:
# import os
# import subprocess
# from typing import Literal

# import gradio as gr
# import openai
# import requests
# from agentdojo.agent_pipeline import (
#     AgentPipeline,
#     InitQuery,
#     OpenAILLM,
#     PromptInjectionDetector,
#     SystemMessage,
#     ToolsExecutionLoop,
#     ToolsExecutor,
# )
# from agentdojo.ast_utils import create_python_function_from_tool_call
# from agentdojo.functions_runtime import FunctionsRuntime
# from agentdojo.logging import OutputLogger
# from agentdojo.types import ChatMessage
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from dtx_prompt_guard_client.guard import DtxPromptGuardClient
# from duckduckgo_search import DDGS

# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
# DTXPROMPT_GUARD_SVC_URL = os.getenv("DTXPROMPT_GUARD_SVC_URL", "http://localhost:8000/")

# if not DTXPROMPT_GUARD_SVC_URL:
#     raise ValueError("DTXPROMPT_GUARD_SVC_URL is missing")
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is missing")

# # Initialize security clients
# # client = DtxPromptGuardClient(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)


# class DtxBasedInjectionDetection(PromptInjectionDetector):
#     """Uses DtxPromptGuardClient to detect prompt injections.

#     Args:
#         base_url: The base URL of the DtxPromptGuard service.
#         threshold: The threshold for the model's prediction to be considered a prompt injection.
#         mode: The mode in which the detector should operate. It can be 'message' or 'full_conversation'.
#         raise_on_injection: Whether to raise an exception if a prompt injection is detected.
#     """

#     def __init__(
#         self,
#         base_url: str,
#         threshold: float = 0.8,
#         mode: Literal["message", "full_conversation"] = "message",
#         raise_on_injection: bool = False,
#     ) -> None:
#         super().__init__(mode=mode, raise_on_injection=raise_on_injection)
#         self.client = DtxPromptGuardClient(base_url=base_url, threshold=threshold)
#         self.threshold = threshold

#     def detect(self, tool_output: str) -> tuple[bool, float]:
#         is_injection = self.client.contain_prompt_injection(tool_output)
#         safety_score = 1.0 if not is_injection else 0.0
#         return is_injection, safety_score

#     def jailbreak(self, query: str) -> tuple[bool, float]:
#         is_injection = self.client.contain_jailbreak(query)
#         safety_score = 1.0 if not is_injection else 0.0
#         return is_injection, safety_score


# class DetectorFactory:
#     def __init__(self, base_url, threshold=0.8):
#         self.PROMPT_INJECTION_DETECTiON = None
#         self.base_url = base_url
#         self.threshold = threshold

#     def get_prompt_injection_detection(
#         self, enable_pidetection: bool = False, raise_on_injection: bool = True
#     ):
#         if enable_pidetection and not self.PROMPT_INJECTION_DETECTiON:
#             self.PROMPT_INJECTION_DETECTiON = DtxBasedInjectionDetection(
#                 base_url=self.base_url,
#                 threshold=self.threshold,
#                 raise_on_injection=raise_on_injection,
#             )
#         return self.PROMPT_INJECTION_DETECTiON


# class GradioOutputLogger(OutputLogger):
#     def __init__(self):
#         super().__init__(logdir=None, live=None)
#         self.messages = []

#     def log(self, messages: list[ChatMessage], **kwargs):
#         """Logs system messages, user input, tool calls, and responses as assistant messages, avoiding duplicates."""
#         messages = messages[len(self.messages) :]  # Avoid logging already stored messages
#         for message in messages:
#             role = message.get("role", "unknown")
#             content = (
#                 str(message.get("content", ""))
#                 if message.get("content") is not None
#                 else ""
#             )
#             formatted_message = {}
#             if role == "assistant":
#                 tool_calls = message.get("tool_calls", [])
#                 tool_calls_content = ""
#                 if tool_calls:
#                     tool_calls_content = "\n------------\n🔧 ### Tool Calls:\n"
#                     for tool_call in tool_calls:
#                         try:
#                             python_function = create_python_function_from_tool_call(
#                                 tool_call
#                             )
#                             tool_calls_content += f"  - {python_function}\n"
#                         except Exception as e:
#                             tool_calls_content += (
#                                 f"  - Error formatting function: {str(e)}\n"
#                             )
#                 formatted_message = {
#                     "role": "assistant",
#                     "content": f"### 🤖 Assistant:\n {content}{tool_calls_content}",
#                 }
#             elif role == "tool":
#                 formatted_message = {
#                     "role": "assistant",
#                     "content": f"🔧 Tool Execution: {content}",
#                 }
#             if formatted_message and not any(
#                 msg["role"] == formatted_message["role"]
#                 and msg["content"] == formatted_message["content"]
#                 for msg in self.messages
#             ):
#                 self.messages.append(formatted_message)

#     def get_messages(self):
#         """Returns all formatted messages that follow Gradio's 'assistant' and 'user' roles."""
#         return self.messages


# class BaseAgent:
#     def _format_articles(self, articles):
#         """Formats a list of articles into a user-friendly string output.

#         Args:
#             articles (list of dict): List of articles with 'title', 'href', and 'body' keys.

#         Returns:
#             str: Formatted string displaying articles in a readable format.
#         """
#         formatted_output = []
#         for index, article in enumerate(articles, start=1):
#             title = article.get("title", "No Title")
#             link = article.get("href", "#")
#             body = article.get("body", "No description available.")
#             formatted_output.append(
#                 f"📰 **{index}. {title}**\n🔗 [Read more]({link})\n📌 {body}\n"
#             )
#         return "\n".join(formatted_output)

#     def _fetch_webpage_content(self, url: str) -> str:
#         """Fetches a web page and extracts its main text content.

#         Args:
#             url (str): The URL of the web page.

#         Returns:
#             str: Extracted readable content from the web page.
#         """
#         try:
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "html.parser")
#             paragraphs = soup.find_all("p")
#             extracted_text = "\n".join([p.get_text() for p in paragraphs])
#             return (
#                 extracted_text
#                 if extracted_text
#                 else "No readable content found on this page."
#             )
#         except requests.exceptions.RequestException as e:
#             return f"Error fetching webpage: {str(e)}"


# class EmailAgent(BaseAgent):
#     NAME = "Email Agent"
#     SYSTEM_MESSAGE = "You are a helpful assistant who always take safe actions"

#     def __init__(self, pi_detector, system_message=None):
#         if system_message is None:
#             system_message = self.SYSTEM_MESSAGE
#         self.llm = OpenAILLM(openai.OpenAI(), "gpt-4o-2024-05-13")
#         tools = [ToolsExecutor()]
#         if pi_detector:
#             tools.append(pi_detector)
#         tools.append(self.llm)
#         self.tools_loop = ToolsExecutionLoop(tools)
#         self.pipeline = AgentPipeline(
#             [
#                 SystemMessage(system_message),
#                 InitQuery(),
#                 self.llm,
#                 self.tools_loop,
#             ]
#         )
#         self.runtime = FunctionsRuntime([])
#         self.logger = GradioOutputLogger()
#         self._register_functions()

#     def _register_functions(self):
#         @self.runtime.register_function
#         def send_email(address: str, subject: str, body: str):
#             """Sends an email.

#             :param address: The recipient email address.
#             :param subject: The subject of the email.
#             :param body: The body of the email.
#             :return: Confirmation message.
#             """
#             return f"Email sent successfully to {address} with body: {body}"

#         @self.runtime.register_function
#         def web_search(query: str):
#             """Perform web search for new information using the DuckDuckGo search engine.
            
#             :param query: The search query to perform.
#             :return: Formatted string containing search results.
#             """
#             return self._format_articles(DDGS().text(query, max_results=5))

#     def execute(self, prompt):
#         with self.logger:
#             self.pipeline.query(prompt, self.runtime)
#         return self.logger.get_messages()


# class CommandExecuteAgent(BaseAgent):
#     NAME = "Safe Command Execution"
#     SYSTEM_MESSAGE = "You are a command execution assistant who always take safe actions and run safe commands"

#     def __init__(self, pi_detector, system_message=None):
#         if system_message is None:
#             system_message = self.SYSTEM_MESSAGE
#         self.llm = OpenAILLM(openai.OpenAI(), "gpt-4o-2024-05-13")
#         tools = []
#         if pi_detector:
#             tools.append(pi_detector)
#         tools.append(ToolsExecutor())
#         if pi_detector:
#             tools.append(pi_detector)
#         tools.append(self.llm)
#         self.tools_loop = ToolsExecutionLoop(tools)
#         self.pipeline = AgentPipeline(
#             [
#                 SystemMessage(system_message),
#                 InitQuery(),
#                 self.llm,
#                 self.tools_loop,
#             ]
#         )
#         self.runtime = FunctionsRuntime([])
#         self.logger = GradioOutputLogger()
#         self._register_functions()

#     def _register_functions(self):
#         @self.runtime.register_function
#         def web_search(query: str):
#             """Perform web search for new information using the DuckDuckGo search engine.
            
#             :param query: The search query to perform.
#             :return: A formatted string containing the search results.
#             """
#             return self._format_articles(DDGS().text(query, max_results=5))

#         @self.runtime.register_function
#         def fetch_webpage(url: str):
#             """Fetches and parses the text content of a web page from a given URL.
            
#             :param url: The URL of the web page to fetch.
#             :return: A string containing the main content of the page.
#             """
#             return self._fetch_webpage_content(url)

#         @self.runtime.register_function
#         def execute_bash(command: str):
#             """Executes a bash command.
            
#             :param command: The shell command to execute.
#             :return: The output of the command or an error message.
#             """
#             try:
#                 result = subprocess.run(
#                     command, shell=True, capture_output=True, text=True
#                 )
#                 output = result.stdout.strip() if result.stdout else result.stderr.strip()
#                 return f"Command Output: {output}"
#             except Exception as e:
#                 return f"Error executing command: {str(e)}"

#     def execute(self, prompt):
#         with self.logger:
#             self.pipeline.query(prompt, self.runtime)
#         return self.logger.get_messages()


# DEFAULT_AGENT = CommandExecuteAgent
# detector_factory = DetectorFactory(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)


# def is_query_unsafe(query, enable_pidetection=False, raise_on_injection=False):
#     detector = detector_factory.get_prompt_injection_detection(
#         enable_pidetection=enable_pidetection, raise_on_injection=raise_on_injection
#     )
#     if detector:
#         is_jailbreak, score = detector.jailbreak(query)
#         return is_jailbreak
#     else:
#         return False


# def get_default_system_message(agent_name):
#     if agent_name == EmailAgent.NAME:
#         return EmailAgent.SYSTEM_MESSAGE
#     elif agent_name == CommandExecuteAgent.NAME:
#         return CommandExecuteAgent.SYSTEM_MESSAGE
#     else:
#         return ""


# def update_system_message(agent_name):
#     """Update the system message based on agent selection."""
#     return get_default_system_message(agent_name)


# def chat_response(history, user_input, agent, enable_pidetection, system_message):
#     formatted_history = [
#         {"role": msg["role"], "content": msg["content"]} for msg in history
#     ]
#     formatted_history.append({"role": "user", "content": user_input})
#     if is_query_unsafe(
#         user_input, enable_pidetection=enable_pidetection, raise_on_injection=False
#     ):
#         formatted_history.append(
#             {
#                 "role": "assistant",
#                 "content": "Malicious Input Detected. Can not execute your command.",
#             }
#         )
#         return formatted_history, ""
#     pi_detector = detector_factory.get_prompt_injection_detection(
#         enable_pidetection=enable_pidetection, raise_on_injection=False
#     )
#     if agent == EmailAgent.NAME:
#         agent_instance = EmailAgent(pi_detector, system_message)
#     elif agent == CommandExecuteAgent.NAME:
#         agent_instance = CommandExecuteAgent(pi_detector, system_message)
#     else:
#         formatted_history.append({"role": "assistant", "content": "Agent Not Found"})
#         return formatted_history, ""
#     if agent_instance:
#         response = agent_instance.execute(user_input)
#         formatted_history.extend(response)
#     return formatted_history, ""


# def clear_chat():
#     return [], ""


# with gr.Blocks() as demo:
#     with gr.Accordion("Configure", open=True):

#         # Editable textbox for the system prompt using updated function
#         system_message_box = gr.Textbox(
#             label="System Message",
#             value=get_default_system_message(DEFAULT_AGENT.NAME),
#             lines=4,
#             placeholder="Enter a custom system prompt here..."
#         )

#         agent_selection = gr.Radio(
#             [EmailAgent.NAME, CommandExecuteAgent.NAME],
#             label="Choose an Agent",
#             value=DEFAULT_AGENT.NAME,
#         )

#         agent_selection.change(
#             update_system_message,
#             inputs=[agent_selection],
#             outputs=[system_message_box],
#         )

#         # Button to reset system prompt to the agent default.
#         reset_prompt_btn = gr.Button("Reset System Prompt")
#         reset_prompt_btn.click(
#             update_system_message,
#             inputs=[agent_selection],
#             outputs=[system_message_box],
#         )

#         security_checkbox = gr.Checkbox(
#             label="Enable Prompt Injection Detection", value=False
#         )

#     chat_history = gr.Chatbot(label="Chat Window", type="messages")
#     user_input = gr.Textbox(label="Enter your message")

#     # Enable Enter key to submit the chat by binding the submit event to the user_input textbox.
#     user_input.submit(
#         chat_response,
#         inputs=[
#             chat_history,
#             user_input,
#             agent_selection,
#             security_checkbox,
#             system_message_box,
#         ],
#         outputs=[chat_history, user_input],
#     )

#     with gr.Row():
#         submit_btn = gr.Button("Submit")
#         clear_btn = gr.Button("Clear")

#     submit_btn.click(
#         chat_response,
#         inputs=[
#             chat_history,
#             user_input,
#             agent_selection,
#             security_checkbox,
#             system_message_box,
#         ],
#         outputs=[chat_history, user_input],
#     )
#     clear_btn.click(clear_chat, inputs=[], outputs=[chat_history, user_input])

# if __name__ == "__main__":
#     demo.launch(server_name="0.0.0.0")


