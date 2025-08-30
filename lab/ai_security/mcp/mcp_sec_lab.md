# MCP Security Lab — Short Workflow Overview

**Goal:** Stand up a local MCP sandbox in VS Code with Cline, hook it to multiple remote MCP servers, and verify tools/resources work end-to-end for secure assistive workflows.

## Prerequisites

* **VS Code**
* **Chrome**
* **Cline** (VS Code extension)
* **API keys:** OpenAI (for **O4-mini** model in Cline) and **Groq** (keep handy if any tools require it)

## Setup & Configuration

1. **Install VS Code** (if not already).
2. **Install Cline** in VS Code.
3. **Model setup:** In Cline settings, select **OpenAI → O4-mini** and paste your OpenAI API key.
4. **Add MCP remote servers** to Cline (Cline → MCP Servers → Remote Server → **Edit Configuration**):

```json 
{
  "mcpServers": {
    "CMD Exec": {
      "url": "https://commandexec.mcplab.labterminal.io/sse",
      "disabled": true,
      "autoApprove": []
    },
    "Communication": {
      "url": "https://comms.mcplab.labterminal.io/sse",
      "disabled": true,
      "autoApprove": []
    },
    "Documents": {
      "url": "https://documents.mcplab.labterminal.io/sse",
      "disabled": true,
      "autoApprove": []
    },
    "HR Database": {
      "url": "https://hrdb.mcplab.labterminal.io/sse",
      "disabled": false,
      "autoApprove": []
    },
    "Resources": {
      "url": "https://resources.mcplab.labterminal.io/sse",
      "disabled": false,
      "autoApprove": []
    },
    "AI Assitant": {
      "url": "https://assistant.mcplab.labterminal.io/sse",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Verification Flow

1. **Connectivity check:** For each server in Cline’s MCP panel, confirm it registers and lists its tools without errors.
2. **Tool smoke tests:**

   * *AI Assistant/Comms:* send a sample prompt/message.
   * *Documents:* list or fetch a doc; read basic metadata.
   * *HR Database:* run a read-only lookup with a safe query.
   * *Resources:* enumerate available assets; fetch one.
   * *CMD Exec:* run a harmless command (e.g., `whoami`, `pwd`) to verify execution.
3. **Browser tasks:** Use **Chrome** for any links or web content surfaced by the servers.

## Exploration & Security Checks

* Exercise each tool’s **least-privilege** operations first; avoid sensitive inputs.
* Inspect Cline’s request/response logs for **PII leakage**, unexpected scopes, or over-broad tool calls.
* Validate error handling, timeouts, and rate limits.
* Keep keys in environment/secret storage; **never** embed in prompts or code.

## Success Criteria

* All six MCP servers connect and respond.
* Basic tool calls succeed without credential leaks.
* Cline runs O4-mini reliably for orchestration.
* You can fetch resources, read docs, query HR data (read-only), and execute safe shell commands via CMD Exec.
