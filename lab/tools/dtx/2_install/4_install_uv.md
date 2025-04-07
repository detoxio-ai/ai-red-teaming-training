# Installation Using uv

This guide covers how to install **dtx** using [`uv`](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

`uv` is a great option if you:
- Want faster installations (especially in CI/CD environments).
- Are setting up fresh environments.
- Want to use modern Python packaging tools.

---

## Prerequisites

- **Python** `>= 3.8`
- **uv** installer

---

## Step 1: Install uv

You can install `uv` globally with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:

```bash
uv --version
```

---

## Step 2: Install dtx Core

To install **dtx** without local model dependencies:

```bash
uv pip install dtx
```

This installs the base CLI for:
- Generating scopes
- Generating plans
- Running cloud-based models or using `ddtx` Docker CLI

---

## Step 3: Install dtx with Local Model Support (Recommended)

If you want to run **local models** (e.g., Tiny-LLM, GPT-2, Hugging Face models), install with extras:

```bash
uv pip install dtx[torch]
```

This will install:
- `torch` — Deep learning backend
- `transformers` — Hugging Face model integration

Recommended if:
- You want local/offline model execution
- You want to integrate with Ollama or Hugging Face models

---

## Step 4: Verify Installation

Check if the CLI is available:

```bash
dtx --help
```

You should see a list of available commands.

---

## Notes

- `uv` is optional but recommended for fast, reproducible installations.
- No Docker is required if you install locally with `uv`.
- For cloud models (OpenAI, Hugging Face), remember to configure your environment variables:
  
See: [Environment Variables Setup](install-env-vars.md)

- If you use `ddtx`, ensure Docker is installed.  
  See: [Docker Installation](install-docker.md)

