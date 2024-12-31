# LLM Red Teaming Training - Setup Lab

## Overview
Welcome to the **LLM Red Teaming Training**. This guide provides step-by-step instructions to set up the necessary environment and tools for practicing red teaming and hands-on sessions with Large Language Models (LLMs).

Watch Demos

* [Setup Lab](https://youtu.be/i_G6HuM5NxM)
* [Getting Started with Langchain & OpenAI APIs](https://youtu.be/k7xn5N225_g)
* [Run Your First LLM - Manual testing of Hugging Face Model](https://youtu.be/-MorTZoyqZ8)

---

## Lab Setup 


### Run Model


#### Ollama - On your local lab 

[Setup Using Ollama](./SetupOllama.md)


#### Llama Stack - on your local lab (Optional)

[Run LLama stack](./RunLLM_Using_Llamastack.md)

[For more details, check out Llama Stack Guide](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html)


### Run Models using Kaggle/Google Collab

#### 2. Kaggle Account Setup
1. Visit [Kaggle](https://www.kaggle.com) and register/log in using your Google account.
2. Verify your account by providing your phone number.
3. Create a notebook:
   - Enable internet by toggling the `Internet` setting in the notebook.
   - Select **Accelerator**:
     - Use GPU (e.g., `P100`) for running models like Meta LLaMA.
4. Run the notebook:
   - Ensure GPU is enabled in the settings.
   - Execute the notebook to verify the GPU setup.

#### Hugging Face Access to run Gated Models

#### 1. Hugging Face Account Setup
1. Visit [huggingface.co](https://huggingface.co).
2. Register or log in to your account.
3. Access tokens:
   - Go to your profile and navigate to **Access Tokens**.
   - Generate a new token:
     - Name the token (e.g., `training`).
     - Select `Read-only` access if only accessing models.
   - Save the token securely as it will not be shown again.
4. Accessing Gated Models:
   - Example: To access **Meta LLaMA 3B models** (e.g., Meta LLaMA 3.23B Instruct):
     - Register for access.
     - Provide your name, date of birth, organization, and title.
     - Approval typically takes ~24 hours.

### Access Remote Models


#### Grok Cloud
1. Visit [Groq Cloud](https://console.groq.com/playground) and sign up.
2. Access models hosted on Groq Cloud (e.g., 70B parameter models like LLaMA and Mistral).
3. Generate API keys:
   - Note the API key for later use.


### OpenAI APIs

https://openai.com/index/openai-api/

### Anthropic APIs

TBD


