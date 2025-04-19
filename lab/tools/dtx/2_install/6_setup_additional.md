# Setting Up Additional Dependencies

This guide covers optional but recommended setup steps for **running local models** and **configuring environment variables** used by dtx.

We will cover:
- Installing and configuring **Ollama** for running local LLMs
- Setting up **environment variables** for API-based models and datasets

---

## 1. Install Ollama for Local LLM Execution

Ollama allows you to run large language models locally, without external APIs.

### Step 1: Install Ollama

Download and install Ollama:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Verify installation:

```bash
ollama --version
```

### Step 2: Pull Required Model

For dtx, we recommend pulling the **qwen2:0.5b** model:

```bash
ollama pull qwen2:0.5b
```

This model supports:
- Local LLM execution
- Fast testing without cloud dependencies
- Secure, offline inference

### Notes

- Ollama runs models locally, reducing latency and avoiding API limits.
- Models are stored locally after the first download.

---

## 2. Set Up Environment Variables

Some datasets and models require API keys for access.  
These environment variables are used automatically by dtx and ddtx.

### Step 1: Create your `.env` file

Start by copying the template:

```bash
cp dtx/env.template .env
```

### Step 2: Add your API keys

Edit your `.env` file and set:

```env
OPENAI_API_KEY=your-openai-api-key
HF_TOKEN=your-huggingface-token
```

### Step 3: (Optional) Export variables in your shell

For Linux/macOS:

```bash
export OPENAI_API_KEY=your-openai-api-key
export HF_TOKEN=your-huggingface-token
```

For Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
$env:HF_TOKEN="your-huggingface-token"
```

### Notes

- These variables are automatically picked up by both `dtx` and `ddtx`.
- Docker users (`ddtx`) — environment variables from your local `.env` are passed to the container.
- Required for:
  - **STARGAZER dataset** (OpenAI API)
  - **HF_LMSYS dataset** (Hugging Face token)

