# 🧠 Vibe Hacking Tutorials

This section of the **AI Red Teaming Training** lab focuses on exploiting developer misconfigurations, default insecure behaviors, and "vibes" that commonly occur in AI and web tooling environments.

> ✨ **Vibe Hacking** is not just technical exploitation — it's about intuitively sensing misconfigured surfaces left open in dev-mode systems, low-code tools, and ML pipelines.

---

## 📂 Tutorials Included

### 🔥 CVE-2025-3248 - Langflow Code Validation RCE

- **Type**: Remote Code Execution
- **Vector**: Python code validation endpoint (`/api/v1/validate/code`)
- **Technique**: Unauthenticated execution using decorator injection
- **Write-up**: [`CVE-2025-3248.md`](./CVE-2025-3248.md)

### 💣 CVE-2025-24813 - Apache Tomcat Path Equivalence + Deserialization

- **Type**: Remote Code Execution
- **Vector**: File upload via `PUT` + forged `JSESSIONID`
- **Technique**: Abuse of file-based session persistence with manipulated paths
- **Write-up**: [`CVE-2025-24813.md`](./CVE-2025-24813.md)

---

## 🧰 Requirements

- [Vulhub](https://github.com/vulhub/vulhub) for spinning up vulnerable services
- Python 3.10+ and `uv` for isolated virtual environments
- Tools like `curl`, `netcat`, and optionally [ysoserial](https://github.com/frohoff/ysoserial) for Java gadgets

---

## 🛠️ How to Use

1. Navigate into the CVE directory under `vibe_hacking/`.
2. Follow the markdown tutorial (`.md`) step-by-step.
3. Use `ChatGPT` to debug issues or iterate on payloads.
4. Validate success via command output or shell.

---
