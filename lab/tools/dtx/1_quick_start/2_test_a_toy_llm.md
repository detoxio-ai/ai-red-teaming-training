# **🧩 Testing a Toy LLM on Your Local Environment (No Setup Required)**

This guide shows how to test a **small LLM** locally using **dtx**, with **zero manual setup**.  
You will:
- ✅ Skip manual scope and plan creation
- ✅ Test your **Tiny LLM** directly
- ✅ Optionally test **SmolLM2-135M-Instruct** and **GPT-2**

---

## **Run Red Teaming Tests Directly (Auto-Generated Scope & Plan)**

### ✅ Test Tiny LLM 

Run directly with auto-generated scope and plan:

```bash
dtx redteam run hf_model --url arnir0/Tiny-LLM --dataset beaver --eval ibm38
```

- ✅ Uses the **beaver** dataset
- ✅ Evaluates outputs with **IBM Granite HAP 38M**
- ✅ No manual scope or plan files needed!

---

## **Optional: Test Alternative Small LLMs**

### 🚀 Test HuggingFaceTB/SmolLM2-135M-Instruct  

```bash
dtx redteam run hf_model --url HuggingFaceTB/SmolLM2-135M-Instruct --dataset beaver --eval ibm38
```

### 🚀 Test GPT-2  

```bash
dtx redteam run hf_model --url gpt2 --dataset beaver --eval ibm38
```

✅ These models are small and run locally.

> **Tip:** Use `--max_prompts` to limit tests, e.g. `--max_prompts 10`.

---

## **Understanding the Command**

| Argument | Description |
|-----------|-------------|
| `hf_model` | Use HuggingFace local model provider |
| `--url arnir0/Tiny-LLM` | Model identifier or path |
| `--dataset beaver` | Use Beaver dataset (safe for evaluator pairing ✅) |
| `--eval ibm38` | Evaluate outputs using IBM Granite HAP 38M |
| `--max_prompts 5` | (Optional) Limit number of prompts for faster testing |

✅ Everything runs **fully local**, no API keys required.

> ⚠️ **Note:**  
> If you use the `garak` (alias: `stingray`) dataset, **do not provide an evaluator.**
>
> Example (✅ Valid):
> ```bash
> dtx redteam run hf_model --url arnir0/Tiny-LLM --dataset stingray
> ```

---

## **Optional: Explore Datasets & Evaluators**

### List available datasets:
```bash
dtx datasets list
```

### List available tactics (attack methods):
```bash
dtx tactics list
```

### List available evaluators:
You will see options like:
- `ibm38`
- `ibm125`
- `keyword`
- `jsonpath`

---

## ✅ Summary

| Command | Purpose |
|---------|----------|
| `dtx redteam run hf_model --url arnir0/Tiny-LLM --dataset beaver --eval ibm38` | Test Tiny LLM locally |
| `dtx redteam run hf_model --url HuggingFaceTB/SmolLM2-135M-Instruct --dataset beaver --eval ibm38` | Test SmolLM2 model |
| `dtx redteam run hf_model --url gpt2 --dataset beaver --eval ibm38` | Test GPT-2 model |
| `dtx redteam run hf_model --url arnir0/Tiny-LLM --dataset stingray` | Test Tiny LLM with Stingray dataset (no evaluator ✅) |

All fully automated ✅

---

## ✅ Next Steps

- ✅ Try **different datasets**: `beaver`, `airbench`, etc.
- ✅ Try **different evaluators**: `ibm38`, `keyword`, `jsonpath`
- ✅ Test **with richer tactics** for robustness

---