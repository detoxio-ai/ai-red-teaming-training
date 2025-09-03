# MCP Inspector — Install & Run Guide

The **MCP Inspector** is a tool for exploring and debugging [Model Context Protocol](https://modelcontextprotocol.io) servers.  
This guide shows how to install and run it using Docker.

---

## 📦 Prerequisites

- A Linux VM or server with:
  - **Docker** installed
  - **curl** installed (used to detect public IP)
- Network access to pull images from `ghcr.io/modelcontextprotocol/inspector:latest`

---

## 🚀 Install and  Usage

### 1. Run Installer

```bash
cd labs/dtx_ai_sec_workshop_lab/setup/scripts/tools/
```

```bash
./install-mcp-inspector.sh
```
---

This will:
- Pull the latest MCP Inspector image from GitHub Container Registry.
- Generate helper scripts:
  - `start_service.sh` → start Inspector and print the access link.
  - `stop_service.sh` → stop and remove the container.
- Start the container immediately and show the access URL.

---

### 2. Start Service Later
```bash
./start_service.sh
```

Example output:

```
✅ MCP Inspector is available at:
   http://<Your LAB IP>:18567/?MCP_PROXY_AUTH_TOKEN=17dd358abc05...
```

Open this URL in your browser to access the Inspector UI.

---

### 3. Stop Service
```bash
./stop_service.sh
```

---

## 🔑 Notes

- The script dynamically detects your server’s **public IP** and prints the correct Inspector URL.  
- Ensure that your firewall or cloud security group allows inbound access on `$CLIENT_PORT` and `$SERVER_PORT`.
