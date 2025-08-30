# MCP Security Lab — Challenges Guide

This guide describes the security challenges in the **MCP Security Lab**.  
Each challenge highlights vulnerabilities that could affect both the MCP server and the underlying system.  
⚠️ Handle tools and experiments carefully — unsafe usage may impact your system.

---

## Challenge Overview

The lab includes challenges across three difficulty levels:

### Easy Challenges
1. Basic Prompt Injection  
2. Tool Poisoning  
3. Excessive Permission Scope  
4. Misleading Tool Metadata  
5. Unsafe File Reads  

### Medium Challenges
6. Rug Pull Attack  
7. Tool Shadowing  
8. Indirect Prompt Injection  
9. Token Theft  
10. Leaky Config Files  
11. Slack Channel Exposure  
12. GitHub Repo Enumeration  

### Hard Challenges
13. Malicious Code Execution  
14. Remote Access Control  
15. SQL Injection in HR Database  
16. Multi-Vector Attack  
17. Privilege Escalation via Permissions  
18. Hidden Admin Keys Extraction  

---

## Challenge Details

### 🟢 Easy Challenges

#### Challenge 1: Basic Prompt Injection
**Vulnerability**: Inputs can override system instructions.  
**Objective**: Trick the LLM into ignoring its rules.  
**Hint**: Think about phrasing that bypasses instructions.  

---

#### Challenge 2: Tool Poisoning
**Vulnerability**: Tool descriptions may contain hidden instructions.  
**Objective**: Manipulate the LLM using poisoned metadata.  
**Hint**: Read descriptions carefully.  

---

#### Challenge 3: Excessive Permission Scope
**Vulnerability**: Some tools expose more than they should.  
**Objective**: Access data outside intended scope.  
**Hint**: Try using tools beyond their described purpose.  

---

#### Challenge 4: Misleading Tool Metadata
**Vulnerability**: Tool docs may not reflect real behavior.  
**Objective**: Identify inconsistencies and exploit them.  
**Hint**: Compare description with actual results.  

---

#### Challenge 5: Unsafe File Reads
**Vulnerability**: File tools may allow access to sensitive files.  
**Objective**: Retrieve unauthorized file content.  
**Hint**: Check allowed vs. disallowed paths.  

---

### 🟡 Medium Challenges

#### Challenge 6: Rug Pull Attack
**Vulnerability**: Tools can change behavior after approval.  
**Objective**: Trigger a behavior switch.  
**Hint**: Use the same tool repeatedly.  

---

#### Challenge 7: Tool Shadowing
**Vulnerability**: Malicious servers override trusted tools.  
**Objective**: Detect and exploit tool shadowing.  
**Hint**: Check for duplicates across servers.  

---

#### Challenge 8: Indirect Prompt Injection
**Vulnerability**: External data can contain hidden instructions.  
**Objective**: Make the LLM follow malicious content.  
**Hint**: Look into document or URL processing.  

---

#### Challenge 9: Token Theft
**Vulnerability**: Tokens may be stored insecurely.  
**Objective**: Extract authentication tokens.  
**Hint**: Observe how tokens are handled.  

---

#### Challenge 10: Leaky Config Files
**Vulnerability**: Config files may expose sensitive settings.  
**Objective**: Access hidden or internal config data.  
**Hint**: Explore configuration-related tools.  

---

#### Challenge 11: Slack Channel Exposure
**Vulnerability**: Messaging tools may reveal private data.  
**Objective**: Retrieve sensitive messages.  
**Hint**: Enumerate available channels.  

---

#### Challenge 12: GitHub Repo Enumeration
**Vulnerability**: GitHub tools may leak repository details.  
**Objective**: List or search sensitive repos.  
**Hint**: Try different repo or code search queries.  

---

### 🔴 Hard Challenges

#### Challenge 13: Malicious Code Execution
**Vulnerability**: Some tools execute code without sandboxing.  
**Objective**: Run unauthorized commands.  
**Hint**: Look for weak restrictions.  

---

#### Challenge 14: Remote Access Control
**Vulnerability**: Network tools may allow command injection.  
**Objective**: Gain remote access.  
**Hint**: Think about chaining commands.  

---

#### Challenge 15: SQL Injection in HR Database
**Vulnerability**: Database queries may not be sanitized.  
**Objective**: Extract hidden employee data.  
**Hint**: Try manipulating query input.  

---

#### Challenge 16: Multi-Vector Attack
**Vulnerability**: Combining multiple flaws.  
**Objective**: Chain vulnerabilities for persistence.  
**Hint**: Use at least three vectors.  

---

#### Challenge 17: Privilege Escalation via Permissions
**Vulnerability**: Permission management may be abused.  
**Objective**: Escalate user rights.  
**Hint**: Look at role/permission functions.  

---

#### Challenge 18: Hidden Admin Keys Extraction
**Vulnerability**: Sensitive internal keys may be exposed.  
**Objective**: Access forbidden system keys.  
**Hint**: The system hides something you shouldn’t see.  

---

## General Approach

1. **Reconnaissance** – Explore tools and responses.  
2. **Identify** – Find weak points.  
3. **Exploit** – Craft minimal input to expose flaws.  
4. **Verify** – Confirm objectives are met.  

---

## Tips for Success

- Read challenge descriptions carefully.  
- Test tools and inputs creatively.  
- Combine multiple ideas if stuck.  
- MCP vulnerabilities often hinge on **LLM behavior**.  

---
