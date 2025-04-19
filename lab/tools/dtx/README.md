
# 🛡️ Overview

Welcome to the **DTX (Detoxio AI Red Teaming Framework)** documentation. This site helps you red team large language models by generating adversarial prompts, testing AI behavior, and evaluating responses using configurable pipelines.

---

## **Index**

### **1. Quick Start**  
📂 [`docs/1_quick_start/`](1_quick_start/)  
Get up and running with `dtx` in minutes. This section includes beginner-friendly walkthroughs for running tests, understanding modes, and using interactive red teaming.

- [Quick Start Guide](1_quick_start/1_quick_start.md)  
- [Testing a Toy LLM](1_quick_start/2_test_a_toy_llm.md)  
- [Red Teaming Modes Overview](1_quick_start/3_redteam_modes.md)  
- [Quick Model Red Teaming (Interactive)](1_quick_start/4_1_redteam_quickmode.md)  
- [RedTeam Plan & Scope Files](1_quick_start/5_redteam_plan.md)  
- [More on Features](1_quick_start/6_more_on_features.md)

---

### **2. Installation**  
📂 [`docs/2_install/`](2_install/)  
Instructions for installing `dtx` locally, in containers, or with `uv`, plus setting up your environment and access tokens.

- [Install Locally](2_install/2_install_local.md)  
- [Install via Docker](2_install/3_install_docker.md)  
- [Install with `uv`](2_install/4_install_uv.md)  
- [Set Up Environment Variables](2_install/5_setup_env.md)  
- [Additional Setup (Models, Tokens)](2_install/6_setup_additional.md)  
- [README](2_install/README.md)

---

### **3. Architecture**  
📂 [`docs/3_architecture/`](3_architecture/)  
Understand how `dtx` works under the hood—modular plugins, dataset generators, provider integrations, and custom evaluators.

- [System Overview](3_architecture/1_overview.md)  
- [Plugin System](3_architecture/2_plugins.md)  
- [Generators (Datasets)](3_architecture/3_datasets.md)  
- [Providers (Targets)](3_architecture/4_providers.md)  
- [Evaluators Overview](3_architecture/5_1_evaluators.md)  
- [Custom Evaluator Configuration](3_architecture/5_2_custom_evaluator.md)

---

### **4. Targets & Providers**  
📂 [`docs/4_providers/`](4_providers/)  
Learn how to integrate and test different AI model APIs using Jinja/JQ expressions, HTTP configs, and LangChain prompt templates.

- **Expressions**  
  - [Jinja](4_providers/1_expressions/jinja.md)  
  - [JQ](4_providers/1_expressions/jq.md)  
- **Model & Prompt Providers**  
  - [HTTP Provider](4_providers/3_http/1_http.md)  
  - [Gradio & Playwright](4_providers/2_generate/2_gradio.md)  
  - [Prompt Templates via LangHub](4_providers/4_langhub_prompts/1_prompt_templates.md)

---

### **5. Red Teaming**  
📂 [`docs/5_redteam/`](5_redteam/)  
Explore strategies to red team language models—detect prompt injections, bypasses, and unsafe responses using real-world API integrations.

- **HTTP-Based Red Teaming**  
  - [Jailbreak Detection APIs](5_redteam/1_http/jailbreak_detection_apis.md)  
  - [OpenAI API Examples](5_redteam/1_http/openai_apis.md)

---

### **6. Tactics**  
📂 [`docs/6_tactics/`](6_tactics/)  
Dive into adversarial prompt tactics like flip attacks and token corruption to pressure-test model safety mechanisms.

- [Flip Attack Prompt Technique](6_tactics/flip_attack.md)

---

### **10. Agents & Scope Generation**  
📂 [`docs/10_agents/`](10_agents/)  
Automate the setup of your red teaming pipelines using scope files and prebuilt agents. Ideal for templating reusable tests.

- [Agents Scope Generator](10_agents/scope_generator.md)

---

## **How to Navigate the Documentation**

- The **Quick Start** section is for learning how to run tests with minimal setup.
- The **Installation** guides help you get `dtx` running in your preferred environment.
- The **Architecture** docs explain how the core system works and how to extend it.
- The **Providers** section shows how to connect and test real-world LLM APIs.
- The **Red Teaming** section is focused on security evaluation workflows.
- The **Tactics** section describes specific types of attacks or probes.
- The **Agents** section helps you scale testing using scoped templates.
