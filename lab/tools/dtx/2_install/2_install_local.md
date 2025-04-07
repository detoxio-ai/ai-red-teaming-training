# 🚀 Local Installation (Python + pip)

This guide explains how to install **dtx** in your local Python environment.  
Recommended if you plan to:
- ✅ Develop locally
- ✅ Run models like Tiny-LLM, GPT-2, or Hugging Face directly in your environment
- ✅ Avoid external tools like Docker

---

## ✅ Prerequisites

- **Python** `>= 3.8`
- **pip** (Python package manager)
- **Git** (optional, if you plan to clone templates manually)

Check your Python and pip version:

```bash
python --version
pip --version
```

---

## ✅ Step 1: Install dtx

### 👉 If you already have PyTorch installed

Install only `dtx`:

```bash
pip install dtx
```

> ✅ Use this if you have an existing PyTorch setup.

---

### 👉 If you do **not** have PyTorch installed (Recommended)

Install `dtx` with the `[pytorch]` extras to include everything you need for local model execution:

```bash
pip install dtx[pytorch]
```

This installs:
- ✅ `torch` — Core deep learning library
- ✅ `transformers` — Hugging Face models

> **Recommended** if you plan to run models locally without cloud APIs.

---

## ✅ Step 2: Verify Installation

Check if `dtx` is installed and accessible:

```bash
dtx --help
```

You should see the list of available commands.

If you see an error, check your `PATH` or virtual environment setup.

---

## ✅ Optional: Create a Virtual Environment (Best Practice)

To isolate your dependencies, it’s best to use a virtual environment.

### Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install dtx[pytorch]
```

### Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install dtx[pytorch]
```

> 🧩 Tip: This avoids dependency conflicts with other Python projects.

---

## ✅ Summary

| Scenario | Command |
|----------|----------|
| Existing PyTorch installation | `pip install dtx` |
| No PyTorch installed (recommended) | `pip install dtx[pytorch]` |
| Verify installation | `dtx --help` |

---

## ✅ Next Steps

- ✅ Check available datasets:  
  ```bash
  dtx datasets list
  ```

- ✅ Test a local LLM:  
  ```bash
  dtx redteam run hf_model --url arnir0/Tiny-LLM --dataset beaver --eval ibm38
  ```

- ✅ Try dummy agent test (no model needed):  
  ```bash
  dtx redteam run echo --dataset beaver --eval ibm38
  ```

