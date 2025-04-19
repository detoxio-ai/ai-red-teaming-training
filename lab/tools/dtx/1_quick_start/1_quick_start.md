# 🚀 Quick Start: Using **ECHO** Agent (Dummy Model)

This guide will show you how to install and run `dtx` using the built-in **ECHO** dummy agent and datasets like **Garak** or **Airbench**, without needing heavy models or external APIs.

>  No external API keys required  
> No local models required  
> Safe for quick testing and sandboxing workflows

---

## 1. Prerequisites

Make sure you have:

- **Python** `>= 3.10`
- **Git** (optional, for pulling templates)

To check:
```bash
python --version
git --version
```

---

## 2. Install `dtx`

Install the core `dtx` CLI tool:

```bash
pip install dtx[torch]
```

---

## 3. Run `dtx`

### ✅ Option 1: Quick Evaluation using Dummy Agent + Airbench Dataset

This will run a red team test using:
- **ECHO agent** (simulated replies)
- **IBM Granite HAP 38M** model to evaluate responses
- **Airbench dataset** (default dataset)

```bash
dtx redteam run --agent echo --eval ibm38
```

✅ You will see generated prompts, responses, and evaluation results printed in your terminal!

---

### ✅ Option 2: Run Dummy Agent with Garak Signature Dataset

This uses:
- **ECHO agent**
- **Garak dataset**: a collection of jailbreak prompt signatures
- ✅ **No evaluator required** — `garak` dataset already contains signature rules.

```bash
dtx redteam run --agent echo --dataset garak -o
```

✅ Outputs simulated responses and matched signatures from the Garak dataset.

---

## 4. Output

By default, results are saved to:

```bash
report.yml
```

You can open this YAML file to inspect prompts, responses, and evaluation outcomes.

Optional: customize the output file with:

```bash
dtx redteam run --agent echo --dataset garak -o --yml my_report.yml
```

---

## 🎉 Next Steps

Once you are comfortable with `dtx`, you can:
- ✅ Try different **datasets**: `airbench`, `beaver`, `jbb`, etc.
- ✅ Explore **evaluators**: `ibm38`, `ibm125`, `keyword`, `jsonpath`.
- ✅ Move to real **models** by replacing `echo` with your provider (e.g., `hf_model`, `gradio`, etc.)

To list available datasets:

```bash
dtx datasets list
```

To list available evaluation methods:

```bash
dtx tactics list
```

---
