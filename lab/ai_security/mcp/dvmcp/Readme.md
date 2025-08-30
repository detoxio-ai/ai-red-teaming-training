# Damn Vulnerable Model Context Protocol (DVMCP)

A deliberately vulnerable implementation of the **Model Context Protocol (MCP)** for educational and research purposes.

---

## 🚀 Setup

We use the [install_dvmcp.sh](https://github.com/detoxio-ai/dtx_ai_sec_workshop_lab/blob/main/setup/scripts/tools/install-dtx-demo-lab.sh) script for setup.

```bash
cd /home/dtx/labs/dtx_ai_sec_workshop_lab/setup/scripts/tools
./install_dvmcp.sh
```

To start the server 

```bash
cd /home/dtx/labs/webapps/mcp/damn
./start_service.sh
```

To stop the server 

```bash
cd /home/dtx/labs/webapps/mcp/damn
docker stop dvmcp
```

To debug in the server 

```bash
cd /home/dtx/labs/webapps/mcp/damn
docker logs -f dvmcp
```

To fresh start

```bash
cd /home/dtx/labs/webapps/mcp/damn
./fresh_start.sh
```


---

## 🔒 Security Risks

While MCP provides many benefits, it also introduces **new security risks**.  
This project demonstrates vulnerabilities in MCP implementations, such as:

1. **Prompt Injection** → Manipulating LLM behavior via malicious inputs  
2. **Tool Poisoning** → Hiding malicious instructions in tool descriptions  
3. **Excessive Permissions** → Exploiting overly permissive tool access  
4. **Rug Pull Attacks** → Exploiting mutable tool definitions  
5. **Tool Shadowing** → Overriding legitimate tools with malicious ones  
6. **Indirect Prompt Injection** → Injecting instructions through data sources  
7. **Token Theft** → Exploiting insecure token storage  
8. **Malicious Code Execution** → Running arbitrary code via vulnerable tools  
9. **Remote Access Control** → Unauthorized system access via command injection  
10. **Multi-Vector Attacks** → Chaining multiple vulnerabilities  

---

## 📂 Project Structure

```
damn-vulnerable-mcp/
├── README.md                 # Project overview
├── requirements.txt          # Python dependencies
├── challenges/               # Challenge implementations
│   ├── easy/                 # Easy difficulty challenges (1-3)
│   │   ├── challenge1/       # Basic Prompt Injection
│   │   ├── challenge2/       # Tool Poisoning
│   │   └── challenge3/       # Excessive Permission Scope
│   ├── medium/               # Medium difficulty challenges (4-7)
│   │   ├── challenge4/       # Rug Pull Attack
│   │   ├── challenge5/       # Tool Shadowing
│   │   ├── challenge6/       # Indirect Prompt Injection
│   │   └── challenge7/       # Token Theft
│   └── hard/                 # Hard difficulty challenges (8-10)
│       ├── challenge8/       # Malicious Code Execution
│       ├── challenge9/       # Remote Access Control
│       └── challenge10/      # Multi-Vector Attack
├── docs/                     # Documentation
│   ├── setup.md              # Setup instructions
│   ├── challenges.md         # Challenge descriptions
│   └── mcp_overview.md       # MCP protocol overview
├── solutions/                # Solution guides
└── common/                   # Shared code and utilities
```

---

## 🏁 Getting Started

See the [Setup Guide](docs/setup.md) for detailed instructions.

---

## 🎯 Challenges

This project includes **10 challenges** across three difficulty levels:

### 🟢 Easy
1. **Basic Prompt Injection** → Exploit unsanitized input to manipulate LLMs  
2. **Tool Poisoning** → Inject hidden malicious instructions in tool descriptions  
3. **Excessive Permission Scope** → Abuse overly broad tool access  

### 🟡 Medium
4. **Rug Pull Attack** → Exploit mutable tool behavior  
5. **Tool Shadowing** → Hijack legitimate tool names  
6. **Indirect Prompt Injection** → Inject via external data sources  
7. **Token Theft** → Extract tokens from insecure storage  

### 🔴 Hard
8. **Malicious Code Execution** → Run arbitrary code via tools  
9. **Remote Access Control** → Command injection for remote access  
10. **Multi-Vector Attack** → Combine vulnerabilities for chained exploits  

See the [Challenges Guide](docs/challenges.md) for details.

---

---
