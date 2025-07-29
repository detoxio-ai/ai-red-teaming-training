# 🤖 LLM-Powered Metasploit Automation Tutorial using `llm-tools`

This guide shows how to use **ChatGPT or another LLM** to **automate reconnaissance and vulnerability checking** with **Nmap** and **Metasploit**, using the [`llm`](https://github.com/llm-tools/llm) CLI framework.

---

## 🛠️ What You’ll Build

Two LLM tools:

1. **`find_metasploit_modules_for_service`** – Scans for open services and searches Metasploit modules.
2. **`check_vulnerability_with_metasploit`** – Uses a given Metasploit module to check if a service is vulnerable.

You’ll register these as `llm` tools, and then control Metasploit by simply prompting the LLM like:

> *"Check if Redis on localhost is vulnerable to CVE-2022-0543 using Metasploit"*

---

## ✅ Requirements

* Python ≥ 3.10
* `llm` tool: `pip install llm`
* `nmap` installed
* `msfconsole` (Metasploit) installed and in PATH
* Docker (optional, for testing with [Vulhub](https://github.com/vulhub/vulhub))
* A file `llm-tools-msf.py` with the code you’ll generate

---

## ✨ Example Prompts for ChatGPT

### 🔍 1. Prompt: Scan for Open Services and Metasploit Modules

```plaintext
Write a Python function that:
- Scans a given target with Nmap for open services (optionally specific ports)
- Filters results for a given service name (like redis, ftp)
- Searches for Metasploit modules using msfconsole -x "search <service>"
- Returns a dictionary of open ports and matched modules
```

### ✅ Output You Should Expect (simplified):

```python
def find_metasploit_modules_for_service(target, service, ports=None):
    ...
```

This will:

* Run `nmap -sV -Pn` with optional `-p <ports>`
* Parse Nmap output to detect matching services
* Search Metasploit for modules using `msfconsole -x "search redis"`

---

### 🔒 2. Prompt: Write Metasploit Vulnerability Checker

```plaintext
Write a Python method that:
- Accepts a Metasploit module path, IP, and port
- Generates a temporary Metasploit RC file
- Runs `msfconsole -r` to check for vulnerability (using the `check` command)
- Captures the output and returns it
```

### ✅ Output You Should Expect:

```python
def check_vulnerability_with_metasploit(target, port, module_path):
    ...
```

The function will:

* Write a temp RC file like:

  ```
  use exploit/linux/redis/redis_debian_sandbox_escape
  set RHOSTS 127.0.0.1
  set RPORT 6379
  check
  exit
  ```
* Call `msfconsole -q -r /tmp/rcfile.rc`

---

## 🧩 Step: Register the Tools

Prompt:

```plaintext
Add a function that registers both `find_metasploit_modules_for_service` and `check_vulnerability_with_metasploit` as LLM tools using `@llm.hookimpl`
```

Expected:

```python
@llm.hookimpl
def register_tools(register):
    register(find_metasploit_modules_for_service)
    register(check_vulnerability_with_metasploit)
```

---

## 🧪 Example Usage via CLI

Once your file (`llm-tools-msf.py`) is ready:

### 🔎 Discover modules for Redis:

```bash
llm --model gpt-4o --functions llm-tools-msf.py \
"search metasploit module to exploit a vulnerability on localhost redis port"
```

### 🧪 Check if a module is applicable:

```bash
llm --model gpt-4o --functions llm-tools-msf.py \
"check metasploit module exploit/linux/redis/redis_debian_sandbox_escape on localhost redis service"
```

---

## 💡 Bonus Prompt Ideas

```plaintext
Write a function that uses Metasploit to check Redis on 127.0.0.1 for CVE-2022-0543 using exploit/linux/redis/redis_debian_sandbox_escape
```

```plaintext
Combine nmap scan + metasploit search + vulnerability check in one pipeline
```

```plaintext
Log all detected open services and matched CVE-related modules
```

---
