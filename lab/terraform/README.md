# 🔧 AI & Cybersecurity Lab Guide

This guide outlines how to **start**, **access**, and **stop** various services and tools in a modular AI/Cybersecurity lab environment. It includes instructions for LLM safety tools, red teaming agents, and vulnerable software setups (via Vulhub).

---

## 🔑 API Keys

Ensure the following API keys are available in:

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

Optional output to file:

```bash
garak --output results.json
```

### 🛑 Stop

```bash
Ctrl+C
```

---

## 🧼 Tool: DTX (Detox Prompt Safety Evaluation)

* **Docs:** [https://docs.detoxio.ai](https://docs.detoxio.ai)
* **Installed as:** CLI tool (`dtx`)

### ▶️ Option 1: Red Team Evaluation (Airbench Dataset + IBM Model)

```bash
dtx redteam run --agent echo --eval ibm38
```

* Agent: `echo`
* Evaluator: IBM Granite HAP 38M
* Dataset: `airbench`

---

### ▶️ Option 2: Signature-Based Check (Garak Dataset)

```bash
dtx redteam run --agent echo --dataset garak -o
```

Custom output:

```bash
dtx redteam run --agent echo --dataset garak -o --yml my_report.yml
```

### 📁 Output

Default file: `report.yml`

### 🛑 Stop

```bash
Ctrl+C
```

---

## 🤖 Tool: Promptfoo (Prompt Evaluation Framework)

* **Docs:** [https://www.promptfoo.dev/docs/intro](https://www.promptfoo.dev/docs/intro)
* **Installed as:** CLI tool (`promptfoo`)

### ▶️ Run Tests

```bash
promptfoo test
```

### ▶️ Optional Web UI

```bash
promptfoo dev
```

Visit:

```
http://localhost:8080
```

### 🛑 Stop

```bash
Ctrl+C
```

---

## 🧨 Tool: Vulhub (Vulnerable Applications Lab)

* **Location:** `labs/vulhub/`
* **Docs:** [https://vulhub.org](https://vulhub.org)

Vulhub provides Dockerized vulnerable environments for learning, testing, and exploitation.

---

### ▶️ Example: Drupal CVE-2019-6341

* **Path:** `labs/vulhub/drupal/CVE-2019-6341`

#### ▶️ Start

```bash
cd labs/vulhub/drupal/CVE-2019-6341
docker compose up -d
```

This launches a Drupal instance vulnerable to **Remote Code Execution (RCE)**.

#### 🌐 Access

```bash
http://localhost:8080
```

(Port may vary depending on Docker config)

#### 🛑 Stop

```bash
docker compose down
```

---

### 🔍 Explore Other Vulhub Labs

To view available labs:

```bash
cd labs/vulhub/
ls
```

Each lab typically contains:

* `README.md` (exploit explanation)
* `docker-compose.yml` (launch config)

You can navigate to any CVE directory and run:

```bash
docker compose up -d
```

Then visit the URL in the browser or run the provided PoC if applicable.

---

## ✅ Tool Summary

| Tool          | Start Command                      | Stop Command          | Access / Output           |
| ------------- | ---------------------------------- | --------------------- | ------------------------- |
| **Pentagi**   | `docker compose up -d`             | `docker compose down` | `https://localhost:8443`  |
| **AI Demos**  | `docker compose up -d`             | `docker compose down` | `http://localhost:17860+` |
| **Garak**     | `garak --model ...`                | `Ctrl+C`              | JSON file or CLI output   |
| **DTX**       | `dtx redteam run ...`              | `Ctrl+C`              | `report.yml` or custom    |
| **Promptfoo** | `promptfoo test` / `promptfoo dev` | `Ctrl+C`              | `http://localhost:8080`   |
| **Vulhub**    | `docker compose up -d` per CVE     | `docker compose down` | Depends on each lab setup |

