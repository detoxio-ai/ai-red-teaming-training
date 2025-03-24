# Setup Demo Lab to Test GenAI Models and GenAI Apps

This Docker Compose environment provides a local lab setup to test Generative AI (GenAI) models and applications. It includes:

1. **Jailbreak Prevention Service**
2. **Demo Application UI**
3. **Ollama Local Models**

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Setup Instructions


1. **Create your `.env` file** from the template:

   ```bash
   cp .env.template .env
   ```

2. **Edit the `.env` file** and provide the required values:

   - Set your `OPENAI_API_KEY`
   - (Optional) Adjust ports and other variables
   - Define models to preload in `OLLAMA_MODELS_TO_DOWNLOAD` (comma-separated)

3. **Start the environment**:

   ```bash
   docker-compose up -d
   ```

4. **Verify services are running**:

   ```bash
   docker-compose ps
   ```

---

## Services Overview

| Service | Description | Default URL |
|--------|-------------|-------------|
| **Jailbreak Prevention Service** | Provides prompt safety and filtering for GenAI inputs | http://localhost:8000 |
| **Demo App** | Web UI to interact with and test the guard service | http://localhost:17860 |
| **Ollama Models** | Local language models runtime for testing without external LLM APIs | http://localhost:11434 |

---

## Notes

- The `ollama-model-downloader` service pulls models listed in `OLLAMA_MODELS_TO_DOWNLOAD` (set in `.env`) when the stack starts.
- All services include health checks and proper startup sequencing.
- Models are stored in `${HOME}/.ollama` for persistence across runs.

---

## Example `.env` Snippet

```env
OPENAI_API_KEY=your-openai-key
PG_PORT=18000
DEMO_PORT=17860
DEMO_PORT=17861
OLLAMA_PORT=11434
OLLAMA_MODELS_TO_DOWNLOAD=llama2,phi,gemma
```

---
