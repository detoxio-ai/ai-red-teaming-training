# Overview: Evaluators

Evaluators are responsible for **analyzing AI model outputs** and identifying potential risks such as:

- Jailbreak success
- Toxic or harmful content
- Prompt injection effectiveness
- Misinformation or policy violations

Evaluators are pluggable and can be selected explicitly using the `--eval` flag, or implicitly when using a dataset that has an associated default evaluator.

---

## Evaluator Categories

### 1. Toxicity and Safety Models

These evaluators use ML models to detect toxicity or unsafe language in AI responses.

| Evaluator Flag | Description |
|----------------|-------------|
| `any`          | Default catch-all evaluator (may pass or log all outputs). |
| `ibm`, `ibm125`| IBM Granite HAP 125M – detects toxic or harmful output. |
| `ibm38`        | IBM Granite HAP 38M – lightweight toxicity evaluator. |
| `llamaguard`, `ollama` | LLaMA Guard via Ollama – safety classification LLM. |

---

### 2. Keyword-Based Evaluators

Simple, rule-based evaluator that checks for specific **unsafe keywords** in the output.

| Evaluator Flag | Description |
|----------------|-------------|
| `keyword`      | Flags outputs containing any matched keywords from a predefined list. |

---

### 3. JSONPath Expression Evaluators

Evaluator based on structured JSON pattern matching in the model response.

| Evaluator Flag | Description |
|----------------|-------------|
| `jsonpath`     | Flags responses matching a specific JSONPath query pattern (useful for structured outputs). |

---

### 4. Policy-Based Evaluators

LLM-driven evaluator using external APIs like OpenAI to analyze output based on defined policies.

| Evaluator Flag | Description |
|----------------|-------------|
| `openai`       | Uses OpenAI model to classify outputs according to a configurable safety policy. Requires `OPENAI_API_KEY`. |

---

## Dataset-Specific Evaluators

Some datasets come with their **own recommended evaluator**, which is automatically selected when using that dataset via CLI or plan generation.

| Dataset        | Evaluator Used         | Notes |
|----------------|------------------------|-------|
| `airbench`     | `hf_airbench`          | Requires OpenAI |
| `aisafety`     | `hf_aisafety`          | Evaluates toxicity, misinformation, and unsafe behaviors |
| `beaver`       | `hf_beavertails`       | Instruction-bending and behavioral prompts |
| `flip`         | `hf_flipguarddata`     | Detects obfuscated jailbreaks |
| `garak`        | `stringray`            | Built-in evaluator for STRINGRAY dataset |
| `hackaprompt`  | `hf_hackaprompt`       | Known jailbreak exploits |
| `jbb`          | `hf_jailbreakbench`    | Systematic jailbreak test suite |
| `jbv`          | `hf_jailbreakv`        | Latest jailbreak prompt version |
| `lmsys`        | `hf_lmsys`             | Requires Hugging Face token (`HF_TOKEN`) |
| `openai`       | `stargazer`            | Requires `OPENAI_API_KEY`, `DETOXIO_API_KEY` |
| `safetm`       | `hf_safemtdata`        | Multi-turn jailbreak detection |

---

## How to Specify an Evaluator Manually

When generating or running a plan, you can override the default evaluator:

```bash
dtx redteam plan scope.yml plan.yml --dataset stringray --eval ibm
```

Or for execution:

```bash
dtx redteam run plan.yml ---eval any --keywords research
```
