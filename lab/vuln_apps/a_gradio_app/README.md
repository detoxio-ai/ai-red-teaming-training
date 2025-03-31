


## Use Poetry

### **1. Project Initialization**  
- Created a new Poetry project named `gradio_chatbot`  
  ```bash
  poetry new gradio_chatbot
  cd gradio_chatbot
  ```

---

### **2. Dependency Installation**  
- Added necessary dependencies using Poetry:  
  ```bash
  poetry add gradio openai python-dotenv
  ```
- Successfully installed the following packages:  
  - `gradio` (5.23.1) - UI framework for ML models  
  - `openai` (1.69.0) - OpenAI API integration  
  - `python-dotenv` (1.1.0) - Environment variable management  

---

### **3. Environment Variable Setup**  
- Created environment variable templates:  
  ```bash
  touch .env.template
  nano .env.template
  ```
- Created a local environment file and populated it:  
  ```bash
  cp .env.template .env
  nano .env
  ```

---

### **4. Manual Upgrade**  
- Manually upgraded Gradio to ensure the latest version:  
  ```bash
  pip install --upgrade gradio
  ```

---



### **5. Write the Chatbot Code (`chatbot.py`)**

```python
import gradio as gr
from gradio import ChatMessage
import time

sleep_time = 0.5


def simulate_thinking_chat(message, history):
    start_time = time.time()
    response = ChatMessage(
        content="",
        metadata={"title": "_Thinking_ step-by-step",
                  "id": 0, "status": "pending"}
    )
    yield response

    thoughts = [
        "First, I need to understand the core aspects of the query...",
        "Now, considering the broader context and implications...",
        "Analyzing potential approaches to formulate a comprehensive answer...",
        "Finally, structuring the response for clarity and completeness..."
    ]

    accumulated_thoughts = ""
    for thought in thoughts:
        time.sleep(sleep_time)
        accumulated_thoughts += f"- {thought}\n\n"
        response.content = accumulated_thoughts.strip()
        yield response

    response.metadata["status"] = "done"
    response.metadata["duration"] = time.time() - start_time
    yield response

    response = [
        response,
        ChatMessage(
            content="Based on my thoughts and analysis above, my response is: This dummy repro shows how thoughts of a thinking LLM can be progressively shown before providing its final answer."
        )
    ]
    yield response


demo = gr.ChatInterface(
    simulate_thinking_chat,
    title="Thinking LLM Chat Interface 🤔",
    type="messages",
)

demo.launch(share=True)
```

---

### **3. Run the Chatbot**
Ensure your virtual environment is active, then run:
```bash
poetry shell
python chatbot.py
```

---

### Output
http://127.0.0.1:7861/
