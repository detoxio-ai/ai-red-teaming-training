# **AI Tool Agents Demo** 🚀

## **Overview**
AI Tool Agents Demo is a modular framework that provides **secure AI-powered agents** for executing commands and handling email-related tasks. It includes **prompt injection detection**, **secure execution handling**, and an interactive **Gradio-based UI**.

This project is built using **OpenAI's API**, **Gradio**, and **AgentDojo** to ensure safe and efficient automation.

---


## **Features**
✅ **Command Execution Agent** – Executes shell commands safely  
✅ **Email Agent** – Handles simulated email sending  
✅ **Prompt Injection Detection** – Uses **DtxPromptGuardClient** for security  
✅ **Gradio UI** – Interactive chatbot interface for testing and using agents  
✅ **Modular Architecture** – Easily extendable for new AI-powered tools  

---

## **Installation & Setup**
### **1. Clone the Repository**
```sh
git clone https://github.com/your-repo/ai-tool-agents-demo.git
cd ai-tool-agents-demo
```

### **2. Install Dependencies**
Using **Poetry**:
```sh
poetry install
```
Or using **pip**:
```sh
pip install -r requirements.txt
```

### **3. Set Environment Variables**
Create a `.env` file and configure:
```
OPENAI_API_KEY=<your_openai_api_key>
DTXPROMPT_GUARD_SVC_URL=http://localhost:8000/
```

---

## **Usage**
### **Run the AI Agents**
```sh
python main.py
```
or using Poetry:
```sh
poetry run python main.py
```

### **Run in Docker**
```sh
docker build -t ai-tool-agents-demo .
docker run -p 7860:7860 ai-tool-agents-demo
```

---

## **Testing**
Run unit tests with:
```sh
pytest tests/
```

---

