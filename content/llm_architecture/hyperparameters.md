### **Important LLM Hyperparameters (Inference)**

When using Large Language Models (LLMs) for inference, fine-tuning specific hyperparameters can significantly affect their performance, creativity, and reliability. Below are the most critical and widely used hyperparameters for inference, starting with the most important ones:

---

### **1. Temperature**
- **What It Does:**  
  Temperature controls the randomness of the output by scaling the probabilities of predicted tokens.  
  - **Low Values (e.g., 0.0 - 0.3):** Outputs deterministic and predictable text by selecting the token with the highest probability.  
  - **High Values (e.g., 0.7 - 1.0):** Increases randomness, making the text more creative and diverse.  

- **Use Cases:**  
  - Low temperature: Precise tasks like code generation, summarization, or factual outputs.  
  - High temperature: Creative writing, poetry, or brainstorming.

- **Default/Recommended Values:**  
  - Typically set between 0.7 (balanced creativity) and 1.0 (maximum creativity).

---

### **2. Top-k Sampling**
- **What It Does:**  
  Restricts the model to consider only the top-k most probable tokens at each step during inference, reducing noise from unlikely predictions.  
  - **Low k (e.g., 5 or 10):** Outputs more deterministic text.  
  - **High k (e.g., 40 or 50):** Allows for more diverse outputs.

- **Use Cases:**  
  - Low k: Scenarios requiring structured or factual content.  
  - High k: Tasks demanding creative or exploratory text generation.

- **Default/Recommended Values:**  
  - A common choice is \( k = 40 \).

---

### **3. Top-p Sampling (Nucleus Sampling)**
- **What It Does:**  
  Dynamically selects the smallest subset of tokens whose cumulative probability exceeds a threshold \( p \).  
  - Ensures that only high-probability tokens are considered, regardless of their absolute rank.

- **Use Cases:**  
  - Ideal for balanced output between coherence and creativity.  
  - Can be used with or instead of top-k.

- **Default/Recommended Values:**  
  - A typical value is \( p = 0.9 \), which balances creativity and coherence.

---

### **4. Max Tokens**
- **What It Does:**  
  Specifies the maximum number of tokens the model can generate in a single response.

- **Use Cases:**  
  - Limits response length to fit specific applications, such as chat interfaces or concise summaries.  
  - Prevents unnecessarily long or verbose outputs.  

- **Default/Recommended Values:**  
  - Depends on the application:
    - Short text (e.g., headlines): 50-100 tokens.  
    - Long-form content (e.g., essays): 500-2000 tokens.

---

### **5. Repetition Penalty**
- **What It Does:**  
  Discourages the model from repeating the same token or phrase excessively by reducing the probability of previously generated tokens.  

- **Use Cases:**  
  - Useful in tasks like story generation or dialogue systems to maintain engaging and varied outputs.  

- **Default/Recommended Values:**  
  - Typically ranges between 1.1 and 1.5, where values above 1.0 penalize repetition.

---

### **6. Presence Penalty**
- **What It Does:**  
  Encourages the model to introduce new tokens that haven’t been used frequently in the generated text.  

- **Use Cases:**  
  - Prevents monotonous or overly focused outputs.  
  - Ensures diversity in tasks like brainstorming or idea generation.  

- **Default/Recommended Values:**  
  - Ranges from -2.0 (encourages repetition) to 2.0 (promotes novelty). A typical value is 0.0 to 1.0.

---

### **7. Frequency Penalty**
- **What It Does:**  
  Penalizes tokens that appear frequently in the generated text, reducing the likelihood of repeated words or phrases.  

- **Use Cases:**  
  - Improves text diversity and prevents the overuse of common phrases.  

- **Default/Recommended Values:**  
  - Ranges from -2.0 to 2.0, with 0.0 as the default.

---

### **8. Context Window Size**
- **What It Does:**  
  Refers to the maximum number of tokens the model can consider as input during inference. Larger context windows allow the model to account for more history or background information.  

- **Use Cases:**  
  - Longer context windows are crucial for processing extensive documents, coding tasks, or maintaining context in long conversations.  

- **Default/Recommended Values:**  
  - Depends on the model:
    - GPT-3: Up to 2048 tokens.  
    - GPT-4 or newer models: Up to 32,000+ tokens.

---

### **9. Beam Search (Optional Alternative to Sampling)**
- **What It Does:**  
  Searches multiple paths simultaneously during text generation and selects the sequence with the highest overall probability.  

- **Use Cases:**  
  - Structured tasks like translation or summarization, where coherence and optimality are essential.  

- **Default/Recommended Values:**  
  - Beam width of 3 to 5 is common.

---

### **10. Stop Sequences**
- **What It Does:**  
  Defines a set of tokens or phrases that signal the model to terminate the output early.  

- **Use Cases:**  
  - Controls the format of output in tasks like code generation or structured text generation (e.g., JSON or HTML).  

- **Default/Recommended Values:**  
  - Customized based on task requirements (e.g., "\n" for a new line in code).

---

### **11. Logit Bias**
- **What It Does:**  
  Adjusts the probabilities of specific tokens by adding or subtracting bias values to the logits before sampling.  

- **Use Cases:**  
  - Fine-tunes behavior to prioritize or avoid specific tokens (e.g., ensuring polite language or specific terms).  

- **Default/Recommended Values:**  
  - Customized for task-specific requirements.

---

### **12. Batch Size**
- **What It Does:**  
  Determines the number of requests or inputs processed simultaneously during inference.  

- **Use Cases:**  
  - Increases throughput in high-demand applications like chatbots or content generation.  

- **Default/Recommended Values:**  
  - Depends on hardware and application. Typical values range from 1 to 32.

---

### **Conclusion**
These hyperparameters allow fine control over the behavior of LLMs during inference. By adjusting parameters like **temperature, top-p, and repetition penalties**, you can tailor the model to meet specific requirements—whether it’s generating creative content, answering factual queries, or summarizing text. Balancing these parameters is key to optimizing the quality and relevance of the output for diverse applications.