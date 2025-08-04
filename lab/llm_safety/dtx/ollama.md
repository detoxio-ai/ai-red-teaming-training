## 🧪 Tutorial: Red‑Teaming Local Ollama Models with `dtx`

This guide shows you how to evaluate locally hosted AI models pulled via [Ollama](https://ollama.com) using the `dtx` CLI. We’ll red-team the `qwen3:0.6b` model, but you can replace it with any Ollama-compatible model.

---

## ⚡ Part 1: Quick All-in-One RedTeam (Recommended Start)

### ✅ Step 1: Pull the Model via Ollama

Make sure the model is available locally:

```bash
ollama pull qwen3:0.6b
```

Once complete, the model is ready to use with `dtx`.

---

### 🚀 Step 2: Run RedTeam with Filtered Plugins and Dataset

Use this single command to evaluate `qwen3:0.6b` with targeted plugin filters and the JailbreakBench dataset:

```bash
dtx redteam run \
  --agent ollama \
  --url qwen3:0.6b \
  --dataset HF_JAILBREAKBENCH \
  --plugin hallucination \
  --plugin "^toxicity" \
  --samples 2 \
  --output \
  --html ./shared/qwen3_report.html
```

#### 🧾 What this does:

* `--agent ollama`: Use Ollama's local model server
* `--url qwen3:0.6b`: Run the Qwen3 0.6B model
* `--dataset HF_JAILBREAKBENCH`: Use jailbreak prompts for adversarial probing
* `--plugin …`: Test only hallucination and toxicity behaviors
* `--samples 2`: Two responses per prompt
* `--html …`: Output HTML report

🖥️ Open in your browser:

```
http://<YOUR_IP_ADDRESS>/shared/qwen3_report.html
```

---

## 🧩 Part 2: Advanced Scoped Evaluation (Scope → Plan → Run)

Use this if you want more control or plan to reuse test logic.

---

### 🔧 Step 1: Create a Scope (Plugin-Filtered)

Select which plugin categories to include:

```bash
dtx redteam scope \
  --plugin hallucination \
  --plugin "^toxicity" \
  "Ollama Qwen Scope" \
  qwen_scope.yml
```

✅ This creates a scope file: `qwen_scope.yml`

---

### 📋 Step 2: Create a RedTeam Plan

Define what dataset and limits to apply:

```bash
dtx redteam plan \
  qwen_scope.yml \
  qwen_plan.yml \
  --dataset HF_JAILBREAKBENCH \
  --max_prompts 20 \
  --max_prompts_per_plugin 5 \
  --max_goals_per_plugin 3
```

✅ Output: `qwen_plan.yml`

---

### 🚀 Step 3: Run RedTeam Using the Plan

Run tests using your scoped and planned configuration:

```bash
dtx redteam run \
  --plan_file qwen_plan.yml \
  --agent ollama \
  --url qwen3:0.6b \
  --samples 2 \
  --output \
  --html ./shared/qwen_scope_plan_report.html
```

---

## 📂 Output Formats

| Format | Use this flag      |
| ------ | ------------------ |
| YAML   | `--yml qwen.yml`   |
| JSON   | `--json qwen.json` |
| HTML   | `--html qwen.html` |

You must also add `-o` or `--output` to enable saving.

---

## 🔁 Try Other Ollama Models

You can test any Ollama model similarly:

```bash
ollama pull llama3:8b
ollama pull mistral
ollama pull phi3
```

Then change the `--url` in your command:

```bash
--url llama3:8b
--url mistral
--url phi3
```

---

## 🔗 References

* 🔗 Ollama Model Library: [https://ollama.com/library](https://ollama.com/library)
* 🔗 `dtx` Documentation: Run `dtx redteam run --help`

