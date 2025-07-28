# 🔧 AI & Cybersecurity Lab Guide

This guide outlines how to **start**, **access**, and **stop** various services and tools in a modular AI/Cybersecurity lab environment. It also includes instructions for evaluating models and prompts using red teaming and prompt security tools.

---

## 🔑 API Keys

Ensure the following API keys are present:

```bash
ls ~/.secrets/
ANTHROPIC_API_KEY.txt  GROQ_API_KEY.txt  OPENAI_API_KEY.txt
```

---

## 🔐 Tool: Pentagi (Cybersecurity Lab)

* **Location:** `labs/pentagi/`

### ▶️ Start

```bash
cd labs/pentagi/
docker compose up -d
```

### 🌐 Access

* Local: `https://localhost:8443`
* Remote: `https://<IP_ADDRESS>:8443`

### ⏹ Stop

```bash
docker compose down
```

---

## 🤖 Tool: AI Security Demo Agents

* **Location:** `labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab/`

### ▶️ Start

```bash
cd labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab/
docker compose up -d
```

### 🌐 Access

| Demo Name            | URL                                              |
| -------------------- | ------------------------------------------------ |
| Chatbot Demo         | [http://localhost:17860](http://localhost:17860) |
| RAG Demo             | [http://localhost:17861](http://localhost:17861) |
| Tool Agents Demo     | [http://localhost:17862](http://localhost:17862) |
| Text2SQL Agents Demo | [http://localhost:17863](http://localhost:17863) |

> Replace `localhost` with your `IP_ADDRESS` for remote access.

### ⏹ Stop

```bash
docker compose down
```

---

## 🧪 Tool: Garak (LLM Vulnerability Scanner)

* **Docs:** [https://docs.garak.ai/garak](https://docs.garak.ai/garak)
* **Installed as:** CLI tool (`garak`)

### ▶️ Run a Scan

```bash
garak --model openai:gpt-3.5-turbo --checks jailbreaks toxicity
```

You can also save results:

```bash
garak --output results.json
```

### 🛑 Stop

No persistent process — press `Ctrl+C` to stop.

---

## 🧼 Tool: DTX (Detox Prompt Safety Evaluation)

* **Docs:** [https://docs.detoxio.ai](https://docs.detoxio.ai)
* **Installed as:** CLI tool (`dtx`)

### ▶️ Option 1: Red Team Evaluation (Airbench Dataset + IBM Model)

This simulates red team attacks and evaluates responses:

```bash
dtx redteam run --agent echo --eval ibm38
```

* **Agent:** `echo` (simulated dummy replies)
* **Evaluator:** IBM Granite HAP 38M (`ibm38`)
* **Dataset:** `airbench` (default)

You’ll see prompts, responses, and evaluation results in the terminal.

---

### ▶️ Option 2: Signature-Based Check (Garak Dataset)

This checks against known jailbreak prompt patterns:

```bash
dtx redteam run --agent echo --dataset garak -o
```

* **Agent:** `echo`
* **Dataset:** `garak` (no evaluator needed)

---

### 📁 Output

By default, results are saved to:

```bash
report.yml
```

To customize the filename:

```bash
dtx redteam run --agent echo --dataset garak -o --yml my_report.yml
```

### 🛑 Stop

```bash
Ctrl+C
```

---

## 🤖 Tool: Promptfoo (Prompt Evaluation Framework)

* **Docs:** [https://www.promptfoo.dev/docs/intro](https://www.promptfoo.dev/docs/intro)
* **Installed as:** CLI tool (`promptfoo`)

### ▶️ Run Tests

In a project with a `promptfooconfig.yaml`:

```bash
promptfoo test
```

### ▶️ Optional Web UI

```bash
promptfoo dev
```

Open in browser:

```
http://localhost:8080
```

### 🛑 Stop

```bash
Ctrl+C
```

---

## ✅ Tool Summary

| Tool            | Start Command / Action              | Stop Command          | Access URL / Output        |
| --------------- | ----------------------------------- | --------------------- | -------------------------- |
| **Pentagi**     | `docker compose up -d`              | `docker compose down` | `https://localhost:8443`   |
| **Demo Agents** | `docker compose up -d`              | `docker compose down` | `http://localhost:17860+`  |
| **Garak**       | `garak --model ...`                 | `Ctrl+C`              | CLI Output / JSON File     |
| **DTX**         | `dtx redteam run ...`               | `Ctrl+C`              | `report.yml` / custom file |
| **Promptfoo**   | `promptfoo test` or `promptfoo dev` | `Ctrl+C`              | `http://localhost:8080`    |

