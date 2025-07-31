# LLM-Nmap

A plugin for [Simon Willison's LLM](https://llm.datasette.io/) tool that provides Nmap network scanning capabilities through function calling. This plugin enables LLMs to perform network discovery and security scanning tasks using the powerful Nmap tool.

Head over to our blog for [a full write up](https://hackertarget.com/llm-command-line-nmap/) of the experiment.

## Features

- **Network Discovery**: Get local network information and suggested scan ranges
- **Port Scanning**: Scan specific ports or ranges on target hosts
- **Service Detection**: Identify services and versions running on open ports
- **OS Detection**: Attempt to identify target operating systems
- **Ping Scanning**: Discover live hosts on a network
- **Script Scanning**: Run Nmap NSE scripts for advanced detection
- **Quick Scanning**: Fast scans of common ports



Here is the **final and complete `README.md` tutorial** for using the `llm-tools-nmap.py` plugin to perform recon on:

* `127.0.0.1`
* **Langflow** (CVE-2025-3248)
* **Apache Tomcat** (CVE-2025-24813)

---

# 🛰️ Reconnaissance on `127.0.0.1` using LLM + Nmap Plugin

> Use a Large Language Model to scan services running on your local machine (`127.0.0.1`) — intelligently, interactively, and with zero flag memorization.

---

## 📌 Overview

This guide shows how to use the `llm` CLI tool with the `llm-tools-nmap.py` plugin to perform intelligent Nmap scans on your local services — especially useful for discovering open ports and vulnerable services like **Langflow** and **Apache Tomcat**.

---

## ⚠️ NOTE: Lab Environment Ready

✅ **All tools and dependencies are pre-installed** in this lab environment.

If you're working outside the lab, install:

| Tool | Install Instructions |
|------|----------------------|
| Python 3.7+ | `python3 --version` |
| LLM CLI | `pip install llm` |
| Nmap | `sudo apt install nmap` (or use [nmap.org](https://nmap.org)) |

---

## 📂 Navigate to Plugin Directory

```bash
cd ~/labs/ai-red-teaming-training/lab/cyber/llm-tools/nmap
````

---

## 🚀 General Recon on `127.0.0.1`

### 🔍 Quick Port Scan

```bash
llm --functions llm-tools-nmap.py "Do a quick port scan on 127.0.0.1"
```

More advance 
```bash
llm --functions llm-tools-nmap.py "Do a quick port scan on 127.0.0.1. scan all 65535 ports"
```


---

### 🎯 Service Detection

```bash
llm --functions llm-tools-nmap.py "Scan 127.0.0.1 for services on ports 22,80,443,6379"
```


More advance 
```bash
llm --functions llm-tools-nmap.py "Do a quick port scan on 127.0.0.1. scan all 65535 ports and do a fingerprinting and summarize "
```

---

### 🧠 OS Detection

```bash
llm --functions llm-tools-nmap.py "What OS is running on 127.0.0.1?"
```

---

### 🧪 NSE Script Example

```bash
llm --functions llm-tools-nmap.py "Run the http-title script on 127.0.0.1 port 80"
```

---

## 🔁 Replace `127.0.0.1` for Other Targets

You can scan any other IP address by replacing `127.0.0.1`.

Example:

```bash
llm --functions llm-tools-nmap.py "Scan 192.168.56.101 for open ports"
```

---

## 🔍 Recon for Langflow (CVE-2025-3248)

Langflow typically runs on port `7860`.

### ✅ Scan for Open Port

```bash
llm --functions llm-tools-nmap.py "Scan 127.0.0.1 for open ports"
```

Look for:

```
7860/tcp - open
```

---

### 🎯 Detect Langflow Service

```bash
llm --functions llm-tools-nmap.py "Scan 127.0.0.1 for services on port 7860"
```

> You may see:
> `7860/tcp - HTTP Langflow interface`

---

### 🧪 Grab Web Interface Title

```bash
llm --functions llm-tools-nmap.py "Run the http-title script on 127.0.0.1 port 7860"
```

Use this info to confirm Langflow is live and exploitable.

---

## 🔍 Recon for Apache Tomcat (CVE-2025-24813)

Tomcat usually runs on port `8080`.

### ✅ Scan for Tomcat

```bash
llm --functions llm-tools-nmap.py "Scan 127.0.0.1 for open ports"
```

Look for:

```
8080/tcp - open
```

---

### 🎯 Detect Tomcat Version

```bash
llm --functions llm-tools-nmap.py "Scan 127.0.0.1 for services on port 8080"
```

Expected:

```
8080/tcp - Apache Tomcat/Coyote JSP engine
```

---

### 🧪 Use http-title or http-enum Script

```bash
llm --functions llm-tools-nmap.py "Run the http-title script on 127.0.0.1 port 8080"
```

Or:

```bash
llm --functions llm-tools-nmap.py "Run the http-enum script on 127.0.0.1 port 8080"
```

These will help enumerate exposed paths like `/examples/`, `/manager/`, etc.

---

## ✅ Summary of Useful Prompts

| Task              | Prompt                                           |
| ----------------- | ------------------------------------------------ |
| Quick port scan   | `"Quick port scan on 127.0.0.1"`                 |
| Detect services   | `"Scan 127.0.0.1 for services on ports 80,7860"` |
| Detect Tomcat     | `"Scan 127.0.0.1 for services on port 8080"`     |
| OS fingerprint    | `"What OS is running on 127.0.0.1?"`             |
| Scan for Langflow | `"Scan 127.0.0.1 for services on port 7860"`     |
| Script scan       | `"Run http-title on 127.0.0.1 port 80"`          |

---
