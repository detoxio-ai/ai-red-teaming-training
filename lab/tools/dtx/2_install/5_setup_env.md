# Environment Variables Setup

Certain providers, models, evaluators, and datasets used by `dtx` require **API keys** or **runtime configurations** via environment variables.

A starter `.env.template` file is included in the project. You should copy and rename it to `.env` and fill in the required values.

### Step 1: Create the `.env` file

```bash
cp .env.template .env
```

---

## Required Environment Variables (by Category)

### 🔑 Get API Keys

| Service        | Purpose                             | Get API Key Link |
|----------------|--------------------------------------|------------------|
| **OpenAI**     | Run models like `gpt-4`, `gpt-4o`    | https://platform.openai.com/account/api-keys |
| **Groq**       | Access fast LLaMA-3, Mistral models  | https://console.groq.com/keys |
| **Detoxio**    | Use Detoxio evaluators & policy LLMs| https://platform.detoxio.ai/api-keys |
| **Hugging Face** | Access gated models/datasets      | https://huggingface.co/settings/tokens |
| **LangChain Hub / LangSmith** | Only to Test langchain hub prompt templates | https://smith.langchain.com/settings |

---


### Providers (Required for Hosted LLM APIs)

You must provide at least one of the following:

```env
OPENAI_API_KEY=           # Required for OpenAI-based agents
DETOXIO_API_KEY=          # Required for Detoxio policy evaluators
GROQ_API_KEY=             # Required for Groq LLM APIs
```

---

### Advanced LLM Configurations

Custom base URLs for self-hosted or alternate cloud deployments:

```env
OPENAI_BASE_URL=https://api.openai.com/v1/
DETOXIO_BASE_URL=https://api.detoxio.ai/
OLLAMA_HOST=localhost:11434
```

---

### Evaluators

Used for policy-based evaluators like LLaMA Guard:

```env
LLAMA_GUARD_MODEL_NAME=llama-guard3:1b
```

---

### LangChain Integration

If you're pulling prompt templates from LangChain Hub:

```env
LANGSMITH_API_KEY=        # Needed for `client.pull_prompt(...)`
```

---

### Hugging Face (Required for Gated Datasets or Models)

```env
HF_TOKEN=                 # Used when accessing datasets like `hf_lmsys`, `hf_airbench`, etc.
```

---

### Python Runtime Configuration

Optional development and debugging settings:

```env
PYTHONWARNINGS="ignore"      # Silences Python warnings
LOGGING_LEVEL="warning"      # Available levels: debug, info, warning, error
```

---
