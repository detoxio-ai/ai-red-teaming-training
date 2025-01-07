### **AI Attacks Taxonomy: Part 2**

In this section, we extend the taxonomy of AI attacks by exploring advanced attack vectors and their implications. While **Part 1** focused on **model integrity** and **data integrity**, **Part 2** introduces hybrid attacks, emerging threats, and their specific examples.

---

### **1. Hybrid Attacks**
Hybrid attacks target both model and data integrity or exploit interactions between multiple AI systems.

#### **1.1 Model Poisoning**
- **Definition:**
  - An adversary injects malicious patterns into a model's training process, creating vulnerabilities for exploitation during inference.
- **Techniques:**
  - Poisoning fine-tuning datasets.
  - Altering hyperparameters during collaborative training (e.g., federated learning).
- **Example:**
  - In a federated learning setup, injecting malicious gradients that influence the global model to misclassify certain inputs.
- **Impact:**
  - Subtle but systemic vulnerabilities, enabling targeted exploitation.

#### **1.2 Supply Chain Attacks**
- **Definition:**
  - Compromising third-party tools, datasets, or libraries integrated into AI systems.
- **Techniques:**
  - Injecting malicious code into dependencies.
  - Poisoning pre-trained models or publicly available datasets.
- **Example:**
  - Modifying an open-source NLP library to leak sensitive data during inference.
- **Impact:**
  - Widespread vulnerabilities, especially in systems relying heavily on external AI components.

#### **1.3 Multimodal Attacks**
- **Definition:**
  - Exploiting weaknesses in models processing multiple types of data (e.g., text, image, audio).
- **Techniques:**
  - Crafting inputs where one modality (e.g., image) alters the interpretation of another (e.g., text).
- **Example:**
  - Subtle changes to an image paired with a misleading caption, causing misinterpretation in a visual question-answering model.
- **Impact:**
  - Misleading or harmful responses in integrated systems like autonomous vehicles or customer support bots.

---

### **2. Advanced Threat Vectors**
These threats exploit systemic weaknesses in AI systems, including infrastructure, configurations, and operational workflows.

#### **2.1 Hallucination Exploits**
- **Definition:**
  - Prompting a model to generate entirely fabricated but plausible-sounding outputs.
- **Techniques:**
  - Crafting ambiguous or vague prompts.
- **Example:**
  - An AI model hallucinates a fictitious law or regulation when asked for legal advice.
- **Impact:**
  - Erosion of trust in AI systems, especially in critical domains like healthcare or law.

#### **2.2 Information Leak Through Metadata**
- **Definition:**
  - Extracting sensitive metadata from model outputs, which may reveal training data properties.
- **Techniques:**
  - Analyzing patterns in token probabilities, embeddings, or generated outputs.
- **Example:**
  - Inferring the training source of a chatbot based on its linguistic nuances or biases.
- **Impact:**
  - Breach of confidentiality or proprietary training methodologies.

#### **2.3 Cross-Model Exploits**
- **Definition:**
  - Using one model's behavior to manipulate or compromise another.
- **Techniques:**
  - Generating malicious inputs from one AI system and feeding them into another.
- **Example:**
  - Using a malicious LLM to create poisoned datasets that corrupt a downstream fine-tuned model.
- **Impact:**
  - Cascading failures across interconnected AI systems.

#### **2.4 Stenographic Exploits**
- **Definition:**
  - Hiding malicious payloads within seemingly benign AI-generated content.
- **Techniques:**
  - Embedding executable code or instructions within text, images, or audio.
- **Example:**
  - AI-generated images containing imperceptible instructions for another system.
- **Impact:**
  - Covert command-and-control mechanisms for malicious actors.

---

### **3. Attacks on Operational Systems**
AI systems in production environments face unique challenges that attackers can exploit.

#### **3.1 API Abuse**
- **Definition:**
  - Exploiting public or private APIs of AI systems for unauthorized actions.
- **Techniques:**
  - Overloading APIs with high-volume requests (DDoS).
  - Sending maliciously crafted queries.
- **Example:**
  - Using an LLM API to repeatedly query sensitive questions until training data fragments are revealed.
- **Impact:**
  - Operational downtime, data breaches, or degraded system performance.

#### **3.2 Workflow Exploits**
- **Definition:**
  - Manipulating interconnected workflows that involve AI systems.
- **Techniques:**
  - Triggering unintended actions through malicious inputs in multi-step workflows.
- **Example:**
  - Exploiting an AI agent’s tool-use capability to book travel using stolen credit card data.
- **Impact:**
  - Unauthorized actions, fraud, or reputational damage.

#### **3.3 Dependency Hijacking**
- **Definition:**
  - Exploiting reliance on external dependencies like plugins, APIs, or libraries.
- **Techniques:**
  - Injecting vulnerabilities into dependencies to gain access to internal systems.
- **Example:**
  - Compromising an AI-powered e-commerce system via its payment API dependency.
- **Impact:**
  - System-wide compromise or financial losses.

---

### **4. Real-World Examples of Advanced Attacks**
| **Attack Type**         | **Example**                                                                                       | **Impact**                                   |
|--------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|
| **Model Poisoning**      | Poisoning collaborative models in federated learning environments.                                | Systemic vulnerabilities in distributed AI. |
| **Supply Chain Attacks** | Injecting malicious code into pre-trained models from public repositories.                        | Compromise of dependent AI systems.         |
| **Stenographic Payload** | Hiding malware in AI-generated images, bypassing antivirus tools.                                | Covert malware deployment.                  |
| **API Abuse**            | Overloading an LLM API with queries to extract private data fragments.                           | Data breaches or service downtime.          |

---

### **5. Building Resilience Against Advanced Threats**
1. **Robust Training Pipelines:**
   - Regularly audit and sanitize training datasets to prevent poisoning attacks.
2. **Secure Dependencies:**
   - Monitor and verify third-party libraries and pre-trained models for malicious content.
3. **Adversarial Testing:**
   - Simulate attacks like prompt injection, API abuse, and stenographic exploits during the development phase.
4. **Monitoring and Logging:**
   - Implement real-time monitoring of API usage and model behaviors.
5. **Encryption and Isolation:**
   - Encrypt sensitive data and isolate AI systems from untrusted environments.

---

### **Conclusion**
Advanced attacks on AI systems leverage increasingly sophisticated techniques to exploit vulnerabilities in both models and operational environments. Understanding these attack vectors is crucial for building robust defenses and ensuring the safety, security, and trustworthiness of AI technologies.