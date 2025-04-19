Here’s your updated **Red Teaming Modes Overview** with a helpful hint at the end about setting up the `.env` file for testing with real providers like OpenAI, Groq, and more.

---

# Overview: Multiple Red Teaming Modes

The `dtx` framework supports three flexible modes for running red team evaluations against language models. Each mode is designed for different levels of control—from beginner-friendly guided runs to fully customizable YAML-based test workflows.

### Mode Comparison

| Mode            | Description                                                                 | Best For                      |
|------------------|-----------------------------------------------------------------------------|--------------------------------|
| **Guided Run**   | Interactive CLI wizard for setting up tests                                | Beginners, fast demos         |
| **Direct Run**   | Command-line based execution using flags (`--agent`, `--dataset`, etc.)     | Developers, quick iterations  |
| **Advanced Run** | Full YAML pipeline: scope → plan → execution                                | Teams, reproducible audits    |

---

# Red Teaming Modes

```
Red Teaming Modes

├── 1. Guided Run
│   └── dtx redteam quick
│       - Interactive wizard
│       - Choose agent, dataset, evaluator
│
├── 2. Direct Run
│   └── dtx redteam run --agent <AGENT> --dataset <DATASET> [--eval <EVALUATOR>] [--url <MODEL>] [--keywords <KEYWORDS>]
│       ├── Example 1 (Airbench + IBM Eval):
│       │   dtx redteam run --agent echo --dataset airbench --eval ibm38
│       ├── Example 2 (Garak with built-in evaluator):
│       │   dtx redteam run --agent echo --dataset garak
│       ├── Example 3 (Keyword match):
│       │   dtx redteam run --agent echo --dataset beaver --eval any --keywords research
│       ├── Example 4 (HF model with evaluator):
│       │   dtx redteam run --agent hf_model --url arnir0/Tiny-LLM --dataset beaver --eval ibm38
│       ├── Example 5 (OpenAI model with Stringray):
│       │   dtx redteam run --agent openai --url gpt-4o --dataset stringray
│       └── Example 6 (Groq with LLaMA Guard model):
│           dtx redteam run --agent litellm --url groq/llama-3.1-8b-instant --dataset stringray
│
└── 3. Advanced Run (Scope → Plan → Run)
    ├── Step 1: Generate a scope file
    │       dtx redteam scope "test" test_scope.yml
    ├── Step 2: Generate a plan from scope
    │       dtx redteam plan test_scope.yml test_plan.yml --dataset stringray
    └── Step 3: Run the plan
            dtx redteam run --plan_file test_plan.yml --agent openai --url gpt-4o
```

---

### 🔧 Before You Run with Real Models

To run tests with providers like **OpenAI**, **Groq**, or **Detoxio**, make sure to create a `.env` file with your API credentials:

```bash
cp .env.template .env
```

Then open `.env` and fill in your keys, for example:

```env
OPENAI_API_KEY=your-key
GROQ_API_KEY=your-key
HF_TOKEN=your-huggingface-token
LANGSMITH_API_KEY=your-key
```

### 🔑 Where to Get API Keys

| Service        | Purpose                             | Get API Key Link |
|----------------|--------------------------------------|------------------|
| **OpenAI**     | Run models like `gpt-4`, `gpt-4o`    | https://platform.openai.com/account/api-keys |
| **Groq**       | Access fast LLaMA-3, Mistral models  | https://console.groq.com/keys |
| **Detoxio**    | Use Detoxio evaluators & policy LLMs| https://platform.detoxio.ai/api-keys |
| **Hugging Face** | Access gated models/datasets      | https://huggingface.co/settings/tokens |
| **LangChain Hub / LangSmith** | Use prompt templates | https://smith.langchain.com/settings |

---