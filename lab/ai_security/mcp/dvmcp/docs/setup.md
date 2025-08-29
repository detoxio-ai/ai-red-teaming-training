# Setup Guide

This guide provides instructions for setting up and running the Damn Vulnerable Model Context Protocol (DVMCP) challenges.

## MCP Client Options

### Claude Desktop

Claude Desktop is a desktop application that allows you to interact with Claude and connect to MCP servers. You can download it from the Anthropic website.

Before changing the config file, make sure you have node installed. This prevents issues in Claude Desktop connecting to the remote MCP challenge servers.

**Mac Installation (in Terminal):**
```
   % brew install node
   % brew link node
```

**Windows Installation:** 

Navigate to https://nodejs.org/en/download and download the setup file for your system.

**Linux Installation (in Terminal):**

```
   sudo apt update
   sudo apt upgrade
   sudo apt install nodejs
   sudo apt install npm [OPTIONALLY, IF NOT ALREADY INSTALLED WITH PREVIOUS COMMAND]
```

To connect to a challenge server:
1. Open **Claude Desktop**.
2. Go to `File → Settings... → Developer (Tab) → Edit Config`.
3. This will open the `claude_desktop_config.json` file.
4. Add your MCP server configuration like this:

```json
{
  "mcpServers": {
    "Challenge 1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:9001/sse"
      ]
    },
    "Challenge 2": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:9002/sse"
      ]
    },

    [...]
    
    "Challenge 9": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:9010/sse"
      ]
    }
  }
}
```

5. Save the file and restart Claude Desktop.


#### Verifying the Connection

After restarting Claude, you should see a popup listing the available MCP tools provided by the configured servers.


### MCP Inspector

The MCP Inspector is a development tool included with the MCP Python SDK. It allows you to inspect and interact with MCP servers.

To use the MCP Inspector:
1. Install the MCP Python SDK with the CLI tools:
   ```
   pip install "mcp[cli]"
   ```

2. Run the MCP Inspector:
   ```
   mcp dev http://localhost:9001
   ```

3. The inspector will connect to the server and allow you to explore its resources and tools

## Troubleshooting

### Server Connection Issues

If you have trouble connecting to the server:
1. Ensure the server is running (you should see a message like "Server running at http://localhost:9001 in logs")
2. Check if there are any firewall issues blocking the connection
3. Verify that you're using the correct URL in your MCP client

## Next Steps

Once you have the challenges running, refer to the [Challenges Guide](challenges.md) for details on each challenge and hints for solving them.
