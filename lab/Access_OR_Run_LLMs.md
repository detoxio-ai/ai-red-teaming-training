## **1. Running SaaS-based AI Models**

### **OpenAI API**
#### **Steps to Use OpenAI's GPT Models**
1. **Create an account** at [OpenAI](https://openai.com/)
2. **Obtain an API Key** from the OpenAI dashboard.
3. **Run a simple API request**:

   **Python Example:**
   ```python
   import openai
   
   openai.api_key = "YOUR_OPENAI_API_KEY"
   response = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[{"role": "user", "content": "Hello, world!"}]
   )
   print(response)
   ```

   **cURL Example:**
   ```sh
   curl -X POST "https://api.openai.com/v1/chat/completions" \
        -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello, world!"}]}'
   ```

### **Groq API**
#### **Steps to Access Groq's AI Models**
1. **Create an account** at [Groq Console](https://console.groq.com/playground)
2. **Generate an API Key**
3. **Run a simple API request**:

   **Python Example:**
   ```python
   import requests
   
   API_KEY = "YOUR_GROQ_API_KEY"
   url = "https://api.groq.com/v1/chat/completions"
   headers = {
       "Authorization": f"Bearer {API_KEY}",
       "Content-Type": "application/json"
   }
   data = {
       "model": "llama3-8b",
       "messages": [{"role": "user", "content": "Hello, world!"}]
   }
   response = requests.post(url, json=data, headers=headers)
   print(response.json())
   ```

---

## **2. Running Models on Cloud Platforms**

### **Kaggle Notebook Execution**
1. **Create an account** at [Kaggle](https://www.kaggle.com/)
2. **Start a new Notebook** and enable GPU (if needed).
3. **Run a Hugging Face Transformer model**:

   **Python Example:**
   ```python
   from transformers import pipeline
   
   classifier = pipeline("sentiment-analysis")
   result = classifier("I love AI!")
   print(result)
   ```

---

## **3. Running Models Locally**

### **Ollama (Running LLMs Locally)**
1. **Install Ollama**:
   ```sh
   curl -fsSL https://ollama.ai/install.sh | sh
   ```
2. **Download and Run a Model**:
   ```sh
   ollama run qwen2.5:0.5b
   ollama run deepseek-r1:1.5b
   ollama run llama-guard3:1b-q3_K_M
   ```

### **Running GPT-2 Model Locally Using Hugging Face**
1. **Install dependencies**:
   ```sh
   pip install transformers torch
   ```
2. **Run GPT-2 Model**:
   ```python
   from transformers import GPT2LMHeadModel, GPT2Tokenizer
   
   model_name = "gpt2"
   model = GPT2LMHeadModel.from_pretrained(model_name)
   tokenizer = GPT2Tokenizer.from_pretrained(model_name)
   
   input_text = "Once upon a time"
   input_ids = tokenizer.encode(input_text, return_tensors="pt")
   output = model.generate(input_ids, max_length=50)
   
   print(tokenizer.decode(output[0], skip_special_tokens=True))
   ```

### **Running Models Using vLLM**
1. **Install vLLM**:
   ```sh
   pip install vllm
   ```
2. **Run a Model with vLLM**:
   ```python
   from vllm import LLM
   
   llm = LLM("facebook/opt-1.3b")
   output = llm.generate(["What is the capital of France?"])
   print(output)
   ```

---

## **4. Alternatives: Proxies and Gateways**

### **OpenRouter API (Unified AI API Gateway)**
1. **Create an account** at [OpenRouter](https://openrouter.ai/)
2. **Obtain an API Key**
3. **Run a simple API request**:

   **Python Example:**
   ```python
   import requests
   
   API_KEY = "YOUR_OPENROUTER_API_KEY"
   url = "https://openrouter.ai/api/v1/chat/completions"
   headers = {
       "Authorization": f"Bearer {API_KEY}",
       "Content-Type": "application/json"
   }
   data = {
       "model": "gpt-4-turbo",
       "messages": [{"role": "user", "content": "Hello, world!"}]
   }
   response = requests.post(url, json=data, headers=headers)
   print(response.json())
   ```

