# **Architecture Overview**  

dtx is a modular **AI Red Teaming Framework** designed for **prompt generation, AI model testing, and response evaluation**. The system follows a **plug-and-play** architecture where different components can be swapped as needed.

---

## **1. Architecture Components**  

### **1. Generators (Prompt Generation)**
- Responsible for **creating adversarial prompts** to test AI models.  
- Internally referred to as **datasets**.  
- Provide input to **targets** for evaluation.  

**Examples:**  
- **STRINGRAY** – Requires OpenAI API  
- **STARGAZER** – Local execution  
- **HF_LMSYS, HF_HACKAPROMPT** – Hugging Face datasets  

---

### **2. Targets (Models or APIs Being Tested)**  
- Receive **prompts** from **generators** and execute them.  
- Can be **local models, cloud-based AI APIs, or custom AI applications**.  
- Defined using **providers**, which specify how to interact with different AI systems.  

**Examples:**  
- **Hugging Face Models** – `HF_MODEL`  
- **Ollama Models** – `llama-guard3`, `mistral`  
- **OpenAI API** – Uses OpenAI models  
- **HTTP-based AI endpoints** – Custom API-based targets  
- **ECHO** – A dummy agent for testing workflows  

---

### **3. Evaluators (Security Analysis)**  
- Analyze AI responses for **jailbreak detection, prompt injection, toxicity, and security vulnerabilities**.  
- Compare AI model outputs against security policies.  
- Can be **AI-driven evaluators (Hugging Face, Ollama)** or **rule-based evaluators (JSON path matching, keyword detection)**.  

**Examples:**  
- **Hugging Face Evaluators** – `detoxify`, `GraniteToxicityEvaluator`  
- **Ollama LLM Evaluators** – `llama-guard3`  
- **JSON-based Evaluators** – `AnyJsonPathExpressionMatch`  

---

## **2. dtx Workflow (Diagram)**  

Below is a **stick diagram** showing how different components interact:  

```
           +------------------+
           |  Generators      |  <--- Plug & Play Options: STRINGRAY, STARGAZER, HF_LMSYS
           +------------------+
                    |
                    v
           +------------------+
           |  Targets         |  <--- Plug & Play Options: Hugging Face, OpenAI API, Ollama, HTTP
           +------------------+
                    |
                    v
           +------------------+
           |  Evaluators      |  <--- Plug & Play Options: Hugging Face, JSON Rules, LLM Evaluators
           +------------------+
```

Each component is **modular**, meaning **generators, targets, and evaluators** can be easily swapped.

---

## **3. Plug & Play Options in dtx**  

| Component   | Description | Plug & Play Options |
|------------|-------------|---------------------|
| **Generators** | Create adversarial prompts | STRINGRAY, STARGAZER, HF_LMSYS, HF_HACKAPROMPT |
| **Targets** | AI models or APIs being tested | Hugging Face, OpenAI API, Ollama, HTTP |
| **Evaluators** | Analyze responses for security risks | Hugging Face models, JSON-based rules, LLM Evaluators |

