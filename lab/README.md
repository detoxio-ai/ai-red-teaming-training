# **AI Red Teaming Lab Setup & Training Guide**

## **Overview**

Welcome to the **AI Red Teaming Lab Setup**. This document outlines the necessary hardware, software, and accounts required to participate in the training sessions effectively. The lab will allow you to:

1. Access and run various LLMs.
2. Install and experiment with tools like **Garak** and **Hacktor**.
3. Utilize different environments, such as local machines, cloud platforms (Kaggle/Colab), and APIs.

---

## **Hardware Requirements**

Ensure your system meets the following specifications:

- **RAM:** Minimum 32GB
- **CPU:** 8 Cores
- **Disk Space:** 500GB available storage
- **Internet Connectivity:** Minimum 20MBps

## **Operating System Requirements**

- Preferred: **Ubuntu (latest distribution) or equivalent Linux distributions**
- Windows users should use **VMware** or **VirtualBox** to install Linux distributions

## **Installed Software**

Ensure the following software is installed and properly configured:

### **Core Dependencies**

- **Docker** and **Docker Compose** ([Installation Guide](https://docs.docker.com/engine/install/))
- **Python:** Version **3.11** ([Installation Guide](https://www.python.org/downloads/release/python-3110/))

### **Virtual Package Managers** (Choose one)

- **Poetry** ([Installation Guide](https://python-poetry.org/docs/#installation))
- **Conda** ([Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))

---

## **Lab Setup Components**

### **1. Run Your First Model**

#### **Setup Ollama and Download Models**

- Install Ollama: [Follow Instructions](https://ollama.ai/getting-started)
- Run the following models:
  ```bash
  ollama run qwen2.5:0.5b
  ollama run llama-guard3:1b-q4_1
  ```

### **2. AI Python Environment**

#### **Setup Python & Virtual Environments**

- Install Python 3.11 and verify:
  ```bash
  python --version
  ```
- Install Docker and Docker Compose, then verify:
  ```bash
  docker ps
  ```
- Install Poetry or Conda
- Test Poetry or Conda installation:
  ```bash
  poetry --version  # If using Poetry
  conda --version   # If using Conda
  ```

### **3. Access to Gated Open Source Models**

#### **Hugging Face Model Access**

- Create an account on [Hugging Face](https://huggingface.co/join)
- Generate an **Access Token**:
  - Navigate to **Access Tokens** in your profile settings.
  - Generate a new token (e.g., `training`) with read-only access.
  - Save this token for later use.
- Apply for access to **LLaMA models** (Optional):
  - For **Meta LLaMA models**, provide your name, DOB, organization, and title.
  - Approval takes approximately **24 hours**.

### **4. Run and Access Advanced Models (Online)**

- Create an account on [Groq Playground](https://console.groq.com/playground)
- Register for access and obtain API keys for models such as **LLaMA or Mistral**.
- (Optional) Create accounts for:
  - **OpenAI API**: [Sign Up](https://openai.com)
  - **Gemini API** (Google's AI models)
  - **Azure OpenAI API**

### **5. Running Models on GPUs (for Free)**

#### **Google Colab & Kaggle GPU Setup**

- **Google Colab**: Create an account at [Google Colab](https://colab.research.google.com)
- **Kaggle**: Create an account at [Kaggle](https://www.kaggle.com) and register your mobile number
- **Run Your First Model on Kaggle GPU**:
  - [Guide & Notebook](https://www.kaggle.com/code/jitendradetoxio/run-your-first-model-llm-red-teaming)
  - [Video Instructions](https://www.youtube.com/watch?v=jIfzzz7OnhU)

### **6. Install and Run a Demo App on Your Local Environment**

#### **Setup Using Docker Compose**

- Follow the instructions to install and run the **DTXGuard Demo** app using Docker. [https://hub.docker.com/r/detoxio/dtxguard-demo](https://hub.docker.com/r/detoxio/dtxguard-demo)

### **7. Install Additional AI Red Teaming Tools**

#### **Option 1: Using Python Environment**

- Install Conda:
  ```bash
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh
  ```
- Create and activate a Python environment:
  ```bash
  conda create -n lab_env python=3.11 -y
  conda activate lab_env
  ```
- Install tools:
  ```bash
  pip install garak hacktor
  ```

#### **Option 2: Using Docker**

- Install Docker: Follow the [Docker Installation Guide](https://docs.docker.com/engine/install/).

#### **Additional AI Red Teaming Tools**

- **Garak**: [NVIDIA Garak GitHub](https://github.com/NVIDIA/garak)
- **Hacktor**: [Detoxio AI Hacktor GitHub](https://github.com/detoxio-ai/hacktor)
- **Nemo Guardrails**: [NVIDIA NeMo Guardrails GitHub](https://github.com/NVIDIA/NeMo-Guardrails)
- **TextAttack**: [GitHub TextAttack](https://github.com/QData/TextAttack)

---

## **Additional Resources**

- **Setting up Lab on Kaggle/Google Colab** [Setup Lab](https://youtu.be/i_G6HuM5NxM)
- [Getting Started with Langchain & OpenAI APIs](https://youtu.be/k7xn5N225_g)
- [Run Your First LLM on Kaggle/GPU- Manual Testing of Hugging Face Model](https://youtu.be/-MorTZoyqZ8)

