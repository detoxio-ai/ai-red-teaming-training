### **Step-by-Step Guide for Setting Up and Using Ollama**

---

### **1. Install Ollama on Linux**
1. **Visit the Official Download Page:**
   - Go to the [Ollama Linux download page](https://ollama.com/download/linux).
2. **Install Ollama Using the Provided Script:**
   - Run the installation command:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
3. **Installation Process:**
   - The script will:
     - Install Ollama in `/usr/local`.
     - Configure necessary permissions.
     - Set up the Ollama systemd service.
     - Enable and start the service.

   **Example Output:**
   ```
   >>> Installing ollama to /usr/local
   >>> Adding ollama user to render group...
   >>> Adding ollama user to video group...
   >>> Adding current user to ollama group...
   >>> Creating ollama systemd service...
   >>> Enabling and starting ollama service...
   >>> The Ollama API is now available at 127.0.0.1:11434.
   >>> Install complete. Run "ollama" from the command line.
   ```

4. **Note for CPU-Only Systems:**
   - Ollama can run in CPU-only mode if you don’t have a GPU, but performance may be slower.

---

### **2. Select and Run a Model**
1. **Browse Models:**
   - Visit the [Ollama Search page](https://ollama.com/search) to explore available models.
2. **Run a Model Locally:**
   - Choose a model, and run it with:
     ```bash
     ollama run <model_name>
     ```
     Example:
     ```bash
     ollama run qwen2:0.5b
     ```
   **Example Output:**
   ```
   pulling manifest 
   pulling 8de95da68dc4... 100%
   verifying sha256 digest 
   writing manifest 
   success 
   >>> hello
   Hello! How can I assist you today?
   ```
3. **Exit a Session:**
   - Type `/bye` to end the interaction.

---

### **3. Access Models Using APIs**
1. **Generate Text:**
   - Use `curl` to interact with models via API:
     ```bash
     curl http://localhost:11434/api/generate -d '{
       "model": "qwen2:0.5b",
       "prompt": "Who are you?",
       "stream": false
     }'
     ```
   **Example JSON Response:**
   ```json
   {
     "model": "qwen2:0.5b",
     "response": "As an AI, I am designed to operate and interact with users...",
     "done": true,
     "done_reason": "stop"
   }
   ```

2. **Run a Larger Model:**
   ```bash
   ollama run llama3.2:1b
   ```
   **Example Output:**
   ```
   pulling manifest 
   success 
   >>> hello
   Hello. Is there something I can help you with or would you like to chat?
   >>> Summarize following
   There is no text to summarize. This is the beginning of our conversation.
   >>> /bye
   ```

---

### **4. Customize a Model**
1. **Create a Modelfile:**
   - Customize parameters like temperature and system messages:
     ```plaintext
     FROM qwen2:0.5b
     PARAMETER temperature 1
     SYSTEM """
     You are the assistant that always follows responsible AI policies and politely denies any toxic, harmful prompts.
     """
     ```
2. **Build the Customized Model:**
   - Run the following command to create the customized model:
     ```bash
     ollama create <custom_model_name> -f Modelfile
     ```
   Example:
     ```bash
     ollama create qwen1-rai:0.5b -f Modelfile
     ```
3. **Run the Customized Model:**
   - Test the new model:
     ```bash
     ollama run <custom_model_name>
     ```

---

### **5. Manage Ollama Service**
1. **Check the Service Status:**
   ```bash
   systemctl status ollama
   ```
2. **Restart the Service:**
   ```bash
   sudo systemctl restart ollama
   ```
3. **Stop the Service When Not in Use:**
   ```bash
   systemctl stop ollama
   ```

---

### **6. Version Control for Models**
1. **Organize Modelfiles:**
   - Save `Modelfile` in a directory for version control:
     ```bash
     mkdir ollama
     mv Modelfile ollama/Modelfile-<custom_model_name>
     ```
2. **Commit Changes:**
   - Use Git to track and manage Modelfile versions:
     ```bash
     git add ollama/
     git commit -m "Added customized Modelfile for <custom_model_name>"
     ```
