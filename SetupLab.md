### **LLM Red Teaming Training - Lab Setup**

This comprehensive guide walks you through setting up a lab environment to experiment with and run models for red teaming tasks, including the installation of necessary tools, configuring environments, and choosing the appropriate platform.

---

## **Overview**
Welcome to the **LLM Red Teaming Training Lab Setup**.  
This lab will allow you to:
1. Access and run various LLMs.
2. Install and experiment with tools like **Garak** and **Hacktor**.
3. Utilize different environments, such as local machines, cloud platforms (Kaggle/Colab), and APIs.

---

### **Lab Setup Components**

1. **Running Models**
   - Local environments (Linux/Mac recommended).
   - Cloud environments (e.g., Kaggle, Google Colab).
   - Using APIs (Groq, OpenAI, Anthropic).

2. **Tools Installation**
   - Tools like **Garak**, **Hacktor**, and **Nemo Guardrails**.
   - Install using Python environments or Docker containers.

---

### **Run Models on Your Local Environment**

#### **Option A: Ollama**
[Follow Ollama Setup Instructions](./SetupOllama.md)

#### **Option B: Llama Stack**

[Follow Llama Stack Instructions](./RunLLM_Using_Llamastack.md)  

or 

[Follow up Llama Stack Documentation](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html)

---

### **Run Models Using Kaggle or Google Colab**

#### **1. Kaggle Account Setup**
1. Sign up or log in at [Kaggle](https://www.kaggle.com).
2. Verify your account with your phone number.
3. Create a notebook:
   - Enable internet access in notebook settings.
   - Select **GPU Accelerator** (e.g., `P100`).
4. Run your notebook:
   - Ensure GPU is enabled under settings.
   - Install libraries and verify GPU setup.

#### **2. Hugging Face for Gated Models**
1. Sign up or log in at [Hugging Face](https://huggingface.co).
2. Generate an **Access Token**:
   - Navigate to **Access Tokens** in your profile settings.
   - Generate a new token (e.g., `training`) with read-only access.
   - Save this token for later use.
3. Request access to gated models:
   - For **Meta LLaMA** models (e.g., LLaMA 3.23B Instruct), provide your name, DOB, organization, and title.
   - Approval takes approximately 24 hours.

---

### **Access Remote Models**

#### **Groq Cloud**
1. Visit [Groq Cloud Playground](https://console.groq.com/playground).
2. Register for access.
3. Obtain API keys for accessing models, such as LLaMA or Mistral (70B parameter models).

#### **OpenAI APIs**
[Get started with OpenAI APIs](https://openai.com/index/openai-api/)

#### **Anthropic APIs**
Details coming soon.

---

### **Tools Installation (Garak, Hacktor, Nemo Guardrails)**

#### **Option 1: Using Python Environment**
1. Install Conda:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```
2. Create and activate a Python environment:
   ```bash
   conda create -n lab_env python=3.11 -y
   conda activate lab_env
   ```
3. Install tools:
   ```bash
   pip install garak hacktor
   ```

#### **Option 2: Using Docker**
Install Docker:
   Follow the [Docker Installation Guide](https://docs.docker.com/engine/install/).

### **Additional Resources**
- **Garak**: [NVIDIA Garak GitHub](https://github.com/NVIDIA/garak)  
- **Hacktor**: [Detoxio AI Hacktor GitHub](https://github.com/detoxio-ai/hacktor)  
- **Nemo Guardrails**: [NVIDIA NeMo Guardrails GitHub](https://github.com/NVIDIA/NeMo-Guardrails)
- **Setting up Lab on Kaggle/Google Collab** [Setup Lab](https://youtu.be/i_G6HuM5NxM)  
- [Getting Started with Langchain & OpenAI APIs](https://youtu.be/k7xn5N225_g)  
- [Run Your First LLM on Kaggle/GPU- Manual Testing of Hugging Face Model](https://youtu.be/-MorTZoyqZ8)

