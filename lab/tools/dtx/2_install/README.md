# dtx Installation Overview

Welcome to the installation guide for **dtx**, your AI red teaming and evaluation framework.

This document helps you choose the right installation method based on your environment and needs.  
We will only cover installation steps here — for usage instructions, refer to the main user guide.

---

## Installation Options

### 1. Local Python Installation

Use this if you want to run `dtx` directly in your Python environment.

- Recommended for development environments.
- Supports local models with `torch` and `transformers`.

Guide: [Local Installation](2_install_local.md)

---

### 2. Docker Installation (`ddtx`)

Use Docker if you want an isolated environment with no local Python dependencies.

- No need to install `torch` locally.
- Automatically manages dependencies and environment variables.

Guide: [Docker Installation](3_install_docker.md)

---

### 3. Fast Installation Using `uv`

Use `uv` if you want a fast, clean install in new environments.

- Faster dependency resolution.
- Optional support for local models.

Guide: [Install Using uv](4_install_uv.md)

---

### 4. Set Up Additional Dependencies

Includes:
- **Ollama** for running local models like `qwen2:0.5b`
- **Environment variables** for API keys (OpenAI, Hugging Face)

Guide: [Set Up Additional Dependencies](5_setup_additional_dependencies.md)

---

## Optional Installations

### Install Agents Scope Generator

Optional: Install additional tools for automated scope generation.

- Uses AI models to generate scopes interactively.
- Requires model access.

Guide: [Install Agents Scope Generator](install-scope-generator.md)

---

## Recommendations

| Use Case                          | Recommended Method            |
|-----------------------------------|-------------------------------|
| Development / Local Testing       | [Local Installation](2_install_local.md) |
| Production, Isolated Environment  | [Docker Installation](3_install_docker.md) |
| Fast Setup in New Environment     | [Install Using uv](4_install_uv.md) |
| Local Models + API Setup          | [Set Up Additional Dependencies](5_setup_additional_dependencies.md) |

