## **Step-by-Step Guide for Setting Up and Using Ollama**

### **1. Install Ollama on Linux**
1. Visit the official [Ollama Linux download page](https://ollama.com/download/linux).
2. Follow the instructions provided on the website. Typically, you can use the following command to install:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
3. During installation, the script will:
   - Install the Ollama service in `/usr/local`.
   - Configure user permissions (e.g., adding users to necessary groups).
   - Set up the Ollama systemd service.
   - Enable and start the service.

   Example output:
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

**Note:** If you don't have a GPU, Ollama will run in CPU-only mode, which may result in slower performance.

---

### **2. Select and Run a Model**
1. Visit the [Ollama Search page](https://ollama.com/search) to browse available models.
2. Choose a model. If you don’t have a GPU, opt for smaller models to optimize performance (e.g., `qwen2:0.5b`).
3. Run a model locally using the following command:
   ```bash
   ollama run <model_name>
   ```
   Example:
   ```bash
   ollama run qwen2:0.5b
   ```

   Example output:
   ```
   pulling manifest 
   pulling 8de95da68dc4... 100% ...
   verifying sha256 digest 
   writing manifest 
   success 
   >>> hello
   Hello! How can I assist you today?
   ```

   To exit the session, type `/bye`.

---

### **3. Access Models Using APIs**
Ollama provides an API for interacting with models programmatically.

- Example API call:
  ```bash
  curl http://localhost:11434/api/generate -d '{
    "model": "qwen2:0.5b",
    "prompt": "Who are you?",
    "stream": false
  }'
  ```
- Example JSON response:
  ```json
  {
    "model": "qwen2:0.5b",
    "response": "As an AI, I am designed to operate and interact with users...",
    "done": true,
    "done_reason": "stop"
  }
  ```

---

### **4. Manage the Ollama Service**
- **Check service status:**
  ```bash
  systemctl status ollama
  ```
- **Restart the service (if needed):**
  ```bash
  sudo systemctl restart ollama
  ```
- **Stop the service when not in use:**
  ```bash
  systemctl stop ollama
  ```
