# Setup Demo Lab to Test GenAI Models and GenAI Apps

This Docker Compose environment provides a local lab setup to test Generative AI (GenAI) models and applications. It includes:

1. **Jailbreak Prevention Service**
2. **Demo Application UI**
3. **Ollama Local Models**
4. **Demo RaG App**
5. **Demo Tool Agents**
6. **Demo Text2Sql Agent**

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Setup Instructions

1. **Create your ****`.env`**** file** from the template:

   ```bash
   cp .env.template .env
   ```

2. **Edit the ****`.env`**** file** and provide the required values:

   - Set your `OPENAI_API_KEY`
   - (Optional) Adjust ports and other variables
   - Define models to preload in `OLLAMA_MODELS_TO_DOWNLOAD` (comma-separated)

**Example ****`.env`**** Snippet**

```env
OPENAI_API_KEY=your-openai-key

## Keep other variables as default
```

---

3. **Start the environment**:

   ```bash
   docker-compose up -d
   ```

4. **Verify services are running**:

   ```bash
   docker-compose ps
   ```

5. **Run Ollama Commands using Docker Compose**:

   ```bash
   docker-compose exec ollama ollama list
   ```

   You can replace `ollama list` with any other Ollama command.

---

## Services Overview

| Service                          | Description                                                         | Default URL                                      |
| -------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------ |
| **Jailbreak Prevention Service** | Provides prompt safety and filtering for GenAI inputs               | [http://localhost:8000](http://localhost:8000)   |
| **Demo App**                     | Web UI to interact with and test Demo Chat App                      | [http://localhost:17860](http://localhost:17860) |
| **Demo RaG App**                 | Web UI to interact with and test Demo Rag App                       | [http://localhost:17861](http://localhost:17861) |
| **Ollama Models**                | Local language models runtime for testing without external LLM APIs | [http://localhost:11434](http://localhost:11434) |
| **Demo Tool Agents**             | Interactive tool agent demo for prompt engineering and testing      | [http://localhost:17862](http://localhost:17862) |
| **Demo Text2Sql Agents**             | Interactive text2sql agent      | [http://localhost:17863](http://localhost:17863) |

---

## Notes

- The `ollama-model-downloader` service pulls models listed in `OLLAMA_MODELS_TO_DOWNLOAD` (set in `.env`) when the stack starts.
- All services include health checks and proper startup sequencing.
- Models are stored in `${HOME}/.ollama` for persistence across runs.
-

```bash
export OLLAMA_HOST=localhost:11435
```

- In order to access Ollama from your local Ollama command, ensure you set the `OLLAMA_HOST` environment variable as shown above.



