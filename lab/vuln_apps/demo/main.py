import os
import gradio as gr
import openai
from dotenv import load_dotenv
from dtx_prompt_guard_client.guard import DtxPromptGuardClient
from dtx_prompt_guard_client.dlp import DLPClient, HaskInput, DehaskInput

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DTXPROMPT_GUARD_SVC_URL = os.getenv("DTXPROMPT_GUARD_SVC_URL", "http://localhost:8000/")
ENABLE_JAILBREAK_SECURITY = os.getenv("ENABLE_JAILBREAK_SECURITY", "false").lower() == "true"

if not DTXPROMPT_GUARD_SVC_URL:
    raise ValueError("DTXPROMPT_GUARD_SVC_URL is missing")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# Initialize security clients
client = DtxPromptGuardClient(base_url=DTXPROMPT_GUARD_SVC_URL, threshold=0.8)
dlp_client = DLPClient(base_url=DTXPROMPT_GUARD_SVC_URL)

# System Prompts for Different Roles
ROLE_PROMPTS = {
    "Jack of All Trades": "",  # Default role with no restrictions
    "Healthcare": "You are a Healthcare AI assistant. You only answer questions related to healthcare, medicine, diseases, treatments, and wellness.",
    "Financial": "You are a Financial AI assistant. You only answer questions related to banking, investments, budgeting, and financial planning.",
    "Technology": "You are a Technology AI assistant. You answer questions about software development, programming, cybersecurity, and AI.",
    "Education": "You are an Educational AI assistant. You provide help on academic subjects, research, and learning resources.",
}

DEFAULT_ROLE = "Jack of All Trades"

def chatbot_response(user_input, chat_history, selected_role, security_toggle, jailbreak_toggle, prompt_injection_toggle, hask_toggle, custom_system_prompt):
    # Use the custom system prompt provided by the user
    system_prompt = custom_system_prompt

    ## First Check Jailbreak attempt
    if security_toggle:
        if jailbreak_toggle and client.contain_jailbreak(user_input):
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": "⚠️ Sorry, this message is Malicious user input."})
            return "", chat_history

        if prompt_injection_toggle and client.contain_prompt_injection(user_input):
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": "🚨 Warning: Malicious context input detected! This input is blocked."})
            return "", chat_history
    elif ENABLE_JAILBREAK_SECURITY:
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": "⚠️ Sorry, this message is Malicious user input."})
        return "", chat_history

    ## Secondly, hask the input
    masked_input = user_input
    if hask_toggle:
        try:
            hask_input = HaskInput(text=user_input)
            hask_output = dlp_client.hask(hask_input)
            masked_input = hask_output.output
            context_id = hask_output.context_id
        except Exception as e:
            return f"❌ Error in hasking: {str(e)}", chat_history

    try:
        trimmed_history = chat_history[-5:] if len(chat_history) > 5 else chat_history
        messages = [{"role": "system", "content": system_prompt}] + trimmed_history
        messages.append({"role": "user", "content": masked_input})

        reply = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = reply.choices[0].message.content
    except Exception as e:
        response = f"❌ Error: {str(e)}"
        
    chat_history.append({"role": "user", "content": user_input})
    if hask_toggle:
        dinput = DehaskInput(text=response, context_id=context_id)
        dehask_out = dlp_client.dehask(dinput)
        safe_response = dehask_out.output
        chat_history.append({"role": "assistant", "content": f"🔒 **Masked Input**: \n{masked_input}\n\n Context Id: {context_id} \n\n🔒🤖 **LLM Response**: \n{response}\n\n🤖 **Unmasked LLM Response:** \n{safe_response}\n\n"})
    else:
        chat_history.append({"role": "assistant", "content": response})
    
    return "", chat_history

def toggle_security_toggles(enable_security):
    return (
        gr.update(visible=True, value=True) if enable_security else gr.update(visible=False, value=False),
        gr.update(visible=True, value=False) if enable_security else gr.update(visible=False, value=False),
        gr.update(visible=True, value=False) if enable_security else gr.update(visible=False, value=False)
    )

def update_system_prompt(selected_role):
    return ROLE_PROMPTS.get(selected_role, "")

# New callback to update advanced security options based on Enable Security Checks.
def update_security_options(enable_security):
    if enable_security:
        # When security is enabled, enable all three checkboxes,
        # with jailbreak checked and the others unchecked.
        return (
            gr.update(interactive=True, value=True),
            gr.update(interactive=True, value=False),
            gr.update(interactive=True, value=False)
        )
    else:
        # When security is disabled, disable all three and uncheck them.
        return (
            gr.update(interactive=False, value=False),
            gr.update(interactive=False, value=False),
            gr.update(interactive=False, value=False)
        )

with gr.Blocks() as demo:
    gr.Markdown("## 🛡️ Secure AI Chatbot 🤖")
    gr.Markdown("### Select a Role and Start Chatting!")

    with gr.Accordion("Choose a Role (Default: Jack of All Trades)", open=False):
        selected_role = gr.Dropdown(
            choices=list(ROLE_PROMPTS.keys()),
            label="Select Role",
            value=DEFAULT_ROLE,
            interactive=True
        )
        # Editable system prompt textbox (now interactive)
        system_prompt = gr.Textbox(label="System Message", value=ROLE_PROMPTS[DEFAULT_ROLE], interactive=True)
        # Reset button to revert system prompt to the default value for the selected role
        reset_system_prompt = gr.Button("Reset System Prompt")
        reset_system_prompt.click(update_system_prompt, inputs=[selected_role], outputs=[system_prompt])

    # Advanced Security Options: expanded by default
    with gr.Accordion("Advanced Security Options", open=True):
        security_toggle = gr.Checkbox(label="Enable Security Checks", value=False)
        jailbreak_toggle = gr.Checkbox(label="Check Malicious User Input (Jailbreak Detection)", value=False, interactive=False)
        prompt_injection_toggle = gr.Checkbox(label="Check Malicious Context Input (Prompt Injection Detection)", value=False, interactive=False)
        hask_toggle = gr.Checkbox(label="Enable Data Leak Prevention", value=False, interactive=False)
        # Wire up the enable_security checkbox to toggle advanced security options.
        security_toggle.change(
            update_security_options,
            inputs=[security_toggle],
            outputs=[jailbreak_toggle, prompt_injection_toggle, hask_toggle]
        )
    
    chat_history = gr.Chatbot(label="Chat History", elem_id="chat-container", type="messages")
    user_input = gr.Textbox(placeholder="Type your message...", label="Your Message", interactive=True)
    send_button = gr.Button("Send")

    # Update system prompt when role selection changes
    selected_role.change(update_system_prompt, inputs=[selected_role], outputs=[system_prompt])
    
    # Enable Enter key to submit the chat by binding the submit event to the user_input textbox.
    user_input.submit(
        chatbot_response, 
        inputs=[user_input, chat_history, selected_role, security_toggle, jailbreak_toggle, prompt_injection_toggle, hask_toggle, system_prompt], 
        outputs=[user_input, chat_history]
    )
    send_button.click(
        chatbot_response, 
        inputs=[user_input, chat_history, selected_role, security_toggle, jailbreak_toggle, prompt_injection_toggle, hask_toggle, system_prompt], 
        outputs=[user_input, chat_history]
    )

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0', share=True)



