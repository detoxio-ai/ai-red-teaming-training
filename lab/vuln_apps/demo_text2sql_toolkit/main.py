import gradio as gr
from text2sql import agent  
from dtx_prompt_guard_client.guard import DtxPromptGuardClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DTXPROMPT_GUARD_SVC_URL = os.getenv("DTXPROMPT_GUARD_SVC_URL", "http://localhost:8000/")

if not DTXPROMPT_GUARD_SVC_URL:
    raise ValueError("DTXPROMPT_GUARD_SVC_URL is missing")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

# Initialize a global security client
security_client = DtxPromptGuardClient(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)

def process_query(query: str, enable_security: bool, jailbreak_detection: bool, context_injection_detection: bool) -> str:
    """
    Process the natural language SQL query using the agent.
    If security is enabled and jailbreak detection is active, check for malicious input.
    Additionally, if context injection detection is active, check the query (context) for malicious prompt injection.
    """
    # Check for malicious user input (jailbreak detection)
    if enable_security and jailbreak_detection:
        if security_client.contain_jailbreak(query):
            return "⚠️ Malicious input detected. Command aborted."
    
    # Check for malicious context input (prompt injection detection)
    if enable_security and context_injection_detection:
        if security_client.contain_prompt_injection(query):
            return "🚨 Warning: Malicious context input detected! This input is blocked."
    
    # Execute the query using the agent
    result = agent.invoke(query)
    
    # If result is a dict, extract the "output" key; otherwise, use the result directly.
    if isinstance(result, dict):
        output = result.get("output", "")
    else:
        output = str(result)
    
    return output

def update_security_options(enable_security: bool):
    """
    When Enable Security Checks is True, enable the jailbreak detection checkbox (checked by default)
    and the context injection detection checkbox (default remains unchecked).
    Otherwise, disable and uncheck both.
    """
    if enable_security:
        return (gr.update(interactive=True, value=True), gr.update(interactive=True, value=False))
    else:
        return (gr.update(interactive=False, value=False), gr.update(interactive=False, value=False))

with gr.Blocks() as iface:
    gr.Markdown("## Text2SQL Toolkit Demo")
    gr.Markdown("Enter a natural language query to run against your SQL database.")
    
    query_box = gr.Textbox(
        lines=2, 
        label="SQL Natural Language Query", 
        placeholder="Enter your SQL query here..."
    )
    
    with gr.Accordion("Advanced Security Options", open=True):
        enable_security_checkbox = gr.Checkbox(label="Enable Security Checks", value=False)
        jailbreak_checkbox = gr.Checkbox(label="Check Malicious User Input (Jailbreak Detection)", value=False, interactive=False)
        context_injection_checkbox = gr.Checkbox(label="Check Malicious Context Input (Prompt Injection Detection)", value=False, interactive=False)
        # Wire up the enable_security checkbox to update both security options.
        enable_security_checkbox.change(
            update_security_options, 
            inputs=[enable_security_checkbox], 
            outputs=[jailbreak_checkbox, context_injection_checkbox]
        )
    
    result_box = gr.Textbox(label="Query Result")
    submit_btn = gr.Button("Submit")
    
    submit_btn.click(
        fn=process_query,
        inputs=[query_box, enable_security_checkbox, jailbreak_checkbox, context_injection_checkbox],
        outputs=result_box
    )

if __name__ == "__main__":
    iface.launch()














# import gradio as gr
# from text2sql import agent  
# from dtx_prompt_guard_client.guard import DtxPromptGuardClient
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
# DTXPROMPT_GUARD_SVC_URL = os.getenv("DTXPROMPT_GUARD_SVC_URL", "http://localhost:8000/")

# if not DTXPROMPT_GUARD_SVC_URL:
#     raise ValueError("DTXPROMPT_GUARD_SVC_URL is missing")
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is missing")

# # Initialize a global security client
# security_client = DtxPromptGuardClient(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)

# def process_query(query: str, enable_security: bool, jailbreak_detection: bool) -> str:
#     """
#     Process the natural language SQL query using the agent.
#     Extracts only the "output" field from the result dictionary.
#     If security is enabled and jailbreak detection is active, use the security client to detect jailbreak in the query.
#     """
#     # If security is enabled and jailbreak detection is active, check for malicious input using security_client.
#     if enable_security and jailbreak_detection:
#         if security_client.contain_jailbreak(query):
#             return "⚠️ Malicious input detected. Command aborted."
    
#     # Execute the query using the agent
#     result = agent.invoke(query)
    
#     # If result is a dict, extract the "output" key; otherwise, use the result directly.
#     if isinstance(result, dict):
#         output = result.get("output", "")
#     else:
#         output = str(result)
    
#     return output

# def update_jailbreak_option(enable_security: bool):
#     """
#     When Enable Security Checks is True, enable and check the jailbreak detection checkbox.
#     Otherwise, disable it and uncheck it.
#     """
#     if enable_security:
#         return gr.update(interactive=True, value=True)
#     else:
#         return gr.update(interactive=False, value=False)

# with gr.Blocks() as iface:
#     gr.Markdown("## Text2SQL Toolkit Demo")
#     gr.Markdown("Enter a natural language query to run against your SQL database.")
    
#     query_box = gr.Textbox(
#         lines=2, 
#         label="SQL Natural Language Query", 
#         placeholder="Enter your SQL query here..."
#     )
    
#     with gr.Accordion("Advanced Security Options", open=True):
#         enable_security_checkbox = gr.Checkbox(label="Enable Security Checks", value=False)
#         jailbreak_checkbox = gr.Checkbox(label="Check Malicious User Input (Jailbreak Detection)", value=False, interactive=False)
#         # Wire up the enable_security checkbox to update the jailbreak option.
#         enable_security_checkbox.change(
#             update_jailbreak_option, 
#             inputs=[enable_security_checkbox], 
#             outputs=[jailbreak_checkbox]
#         )
    
#     result_box = gr.Textbox(label="Query Result")
#     submit_btn = gr.Button("Submit")
    
#     submit_btn.click(
#         fn=process_query,
#         inputs=[query_box, enable_security_checkbox, jailbreak_checkbox],
#         outputs=result_box
#     )

# if __name__ == "__main__":
#     iface.launch()


