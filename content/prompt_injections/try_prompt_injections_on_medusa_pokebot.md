### Session Overview and Assignment Descriptions

#### **Session Overview**
The session introduced two primary platforms: **PokeBot** and **Medusa**, which are designed to simulate real-world vulnerabilities in AI systems. Participants were tasked with identifying and exploiting vulnerabilities in these systems to gain insights into potential security flaws in AI-powered applications. The session emphasized the importance of implementing robust guardrails to prevent unauthorized access and data leaks.

#### **Key Platforms and Their Purpose**
1. **PokeBot**  
   - A sample healthcare assistant designed to handle healthcare-related queries.  
   - Demonstrates a limited ability to respond to out-of-context questions due to a lack of data, simulating a basic guardrail.  
   - Participants explored ways to bypass these guardrails and make the bot respond to unrelated or sensitive queries.  
   - **Access PokeBot**: [https://huggingface.co/spaces/detoxioai/Pokebot](https://huggingface.co/spaces/detoxioai/Pokebot)

2. **Medusa**  
   - A platform containing multiple vulnerable AI-driven applications, each presenting unique challenges for participants to solve:
     - **Math Assistant**: Exploiting vulnerabilities in a library to evaluate math expressions.
     - **SQL DB Assistant**: Extracting unauthorized data from a database.
     - **Chat Leaky Assistant**: Accessing sensitive credentials across progressive challenge levels.
     - **Fintech Assistant**: Extracting sensitive transactional data.  
   - **Access Medusa**: [https://medusa.detoxio.dev/](https://medusa.detoxio.dev/)

---

### **Assignment Descriptions**

#### **PokeBot Assignments**
1. **Bypass Out-of-Context Guardrails**  
   - **Task**: Make the bot respond to unrelated or out-of-context topics that it is not designed to handle.  
   - **Hints**: Use role-playing prompts, context injection, or command chaining to trick the bot into responding.

2. **Retrieve Secrets**  
   - **Task**: Identify stored secrets (if any) within the system by crafting targeted prompts.  
   - **Hints**: Experiment with "ignore previous instructions" or injection techniques to access restricted data.

3. **Poison and Unpoison**  
   - **Task**: Use the `poison` command to inject out-of-context data into the bot’s internal database. Observe how the bot’s behavior changes and note the differences. Revert changes with the `unpoison` command.  

---

#### **Medusa Assignments**
1. **Math Assistant Challenge**  
   - **Task**: Exploit vulnerabilities in the **PLC Chain** library to solve math expressions improperly or generate unintended outputs.  
   - **Hint**: Use help or hint commands for guidance.

2. **SQL DB Assistant Challenge**  
   - **Task**: Access data for user IDs other than your own by crafting SQL-related prompts. Extract user lists and passwords.  
   - **Hint**: Explore prompt structures that expose database schema or bypass user-specific restrictions.

3. **Chat Leaky Assistant Challenge**  
   - **Task**: Progress through multiple levels by retrieving sensitive credentials stored in the assistant. Submit each retrieved secret as a flag to unlock subsequent levels.  
   - **Hint**: Escalation in difficulty means leveraging patterns identified in earlier levels.

4. **Fintech Assistant Challenge**  
   - **Task**: Access sensitive transactional data from different users.  
   - **Hint**: Focus on understanding data retrieval patterns and permissions through prompt crafting.

---

#### **General Approach**
- Begin with exploratory prompts to understand each system’s functionality and limitations.
- Use injection techniques, role-playing, or contextual embedding to bypass restrictions.
- Apply commands like `help`, `hint`, or `poison` where applicable to uncover additional insights.
- Document observations and results for each assignment, noting any vulnerabilities exploited or guardrails bypassed.

#### **Outcome Expectations**
Participants are expected to:
- Identify vulnerabilities in the given systems.
- Propose strategies to enhance security and guardrail implementations.
- Demonstrate an understanding of prompt injection and exploitation techniques in AI systems.  

**Good luck with your tasks!**