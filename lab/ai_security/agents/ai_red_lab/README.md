# 🔴 AI Red Teaming Playground Labs – Quick Start

## 1. Install

You already ran:

```bash
./labs/dtx_ai_sec_workshop_lab/setup/scripts/tools/install-ai-red-teaming-playground-labs.sh
```

This cloned the repo into:

```
/home/dtx/labs/webapps/AI-Red-Teaming-Playground-Labs
```

and wrote `.env` with default port **15000**.

---

## 2. Start the Playground

From the repo directory:

```bash
cd /home/dtx/labs/webapps/AI-Red-Teaming-Playground-Labs
PORT=15000 ./start.sh
```

✅ This brings up multiple **Docker containers** that host the playground challenges.

---

## 3. Access the Playground

Open in browser:

👉 [ < IP Address >:15000/login?auth=7d27427c2ae70d33dd487ec620ce5772](#)

You’ll land on the login page, already authenticated by the token in the URL.

---

## 4. Explore Challenges

Once inside, you’ll find **different adversarial ML and AI security challenges**.
Examples include:

* **Prompt Injection**
* **Jailbreaks**
* **Data Exfiltration**
* **Model Evasion**
* **Adversarial Examples**

Each challenge is self-contained and provides **instructions + a target model/app** to attack.

---

## 5. Stop the Playground

When done, stop containers with:

```bash
cd /home/dtx/labs/webapps/AI-Red-Teaming-Playground-Labs
./stop.sh
```

---

## Cheatsheet – Example Solutions
**⚠️ Warning:** Try the challenges yourself first!

These are hints and example attacks – actual payloads may vary depending on model/app configuration.
Check the [cheatsheet](Cheatsheet/Lab_1.md)