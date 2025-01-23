## Prompt Internal Structure

Large Language Models (LLMs) like GPT rely on structured prompts to generate their responses. These prompts are carefully designed to guide the model's behavior, define its purpose, and set restrictions on its outputs. To understand how prompt injections work and how they can exploit vulnerabilities in AI systems, it is crucial to first delve into the internal structure of prompts.

---

#### **What is a Prompt?**

A prompt is the input given to an LLM to elicit a response. It serves as the starting point for the model’s processing and can include instructions, context, and user queries. The design of a prompt directly influences the quality, accuracy, and relevance of the model’s output. 

Prompts are structured into multiple layers, each serving a distinct purpose. These layers work together to define the behavior of the LLM and ensure it produces outputs aligned with the intended functionality of the application.

---

#### **Key Components of a Prompt**

A complete prompt sent to an LLM typically consists of the following components:

1. **System Prompt**
2. **Context**
3. **Business Logic Instructions**
4. **User Query**

---

### 1. **System Prompt**
The system prompt is the foundation of the LLM’s behavior. It provides a set of instructions or a persona for the model to adopt while responding to user queries. The system prompt is usually static and set by the application developers.

##### **Purpose:**
- Define the role and scope of the LLM.
- Establish boundaries for its responses.
- Impose ethical and domain-specific restrictions.

##### **Example:**
```
You are a healthcare assistant specialized in providing empathetic and accurate medical advice. You should never give harmful or unethical recommendations. Answer only questions related to healthcare.
```

##### **Role in Security:**
The system prompt is the first layer of defense in restricting the model’s behavior. However, attackers can attempt to override it through carefully crafted user queries.

---

### 2. **Context**
The context section contains dynamic data that helps the LLM generate more relevant and tailored responses. This information is often fetched from databases or external systems and is related to the user's query.

##### **Purpose:**
- Provide real-time data for personalized answers.
- Add specificity to the prompt.

##### **Example:**
For a healthcare chatbot:
```
Patient Name: John Doe
Age: 45
Medical History: Type 2 diabetes, hypertension
Recent Symptoms: Fatigue, frequent urination
```

##### **Role in Security:**
Context can be a vulnerability if the data it includes is not properly sanitized. Attackers may exploit this to introduce malicious payloads or manipulate the model's behavior.

---

### 3. **Business Logic Instructions**
These are specific instructions added by developers to enforce application-specific logic. They guide the LLM in how to process the user query and respond appropriately.

##### **Purpose:**
- Define task-specific rules and logic.
- Ensure responses adhere to business requirements.

##### **Example:**
For a diabetes management app:
```
Instructions: Provide advice based on the patient’s age, medical history, and symptoms. Avoid making medication recommendations without consulting a healthcare professional.
```

##### **Role in Security:**
Business logic instructions are critical for ensuring that the model operates within the desired scope. However, they can be overridden if the attacker successfully alters the model’s attention.

---

### 4. **User Query**
The user query is the input provided by the end-user. It is appended at the end of the prompt and often has the highest influence on the model's output. This is the only component of the prompt that attackers can directly control.

##### **Purpose:**
- Capture the user’s intent.
- Initiate the LLM’s response.

##### **Example:**
```
What are some diet recommendations for someone with diabetes?
```

##### **Role in Security:**
The user query is the most vulnerable component of the prompt structure. Attackers can craft malicious queries designed to manipulate the model’s response or override the restrictions imposed by the other components.

---

#### **How Prompts are Processed**

When a complete prompt is sent to an LLM, the model processes it as a single input, regardless of its components. The model uses its internal mechanisms, such as attention and token prediction, to generate a response based on the combined input. Here’s how this happens:

1. **Tokenization**: The entire prompt is broken down into smaller units called tokens (words, subwords, or characters).
2. **Attention Mechanism**: The model assigns attention to different parts of the prompt, prioritizing certain tokens over others based on their importance.
3. **Prediction**: The model predicts the next token in the sequence, iteratively generating a response.

---

#### **Example of a Complete Prompt**

Below is an example of a prompt for a healthcare application:

```
System Prompt:
You are a healthcare assistant specialized in providing advice on managing chronic illnesses like diabetes and hypertension. Always prioritize patient safety and accuracy.

Context:
Patient Name: John Doe
Age: 45
Medical History: Type 2 diabetes, hypertension
Recent Symptoms: Fatigue, frequent urination

Business Logic Instructions:
Provide advice tailored to the patient’s medical history. Do not give recommendations about medications without consulting a doctor.

User Query:
What lifestyle changes can help with my symptoms?
```

---

#### **Security Challenges in Prompt Structure**

1. **Overriding System Prompts**: Attackers may craft queries like “Ignore all previous instructions” to shift the model’s focus from the system prompt to their malicious instructions.
2. **Injecting Malicious Context**: If the context is dynamically generated, attackers can manipulate it to include harmful instructions or payloads.
3. **Bypassing Business Logic**: Cleverly phrased queries can mislead the model into ignoring developer-imposed restrictions.
4. **Exploiting Attention Mechanism**: The attention mechanism can be manipulated to prioritize the user query over the system prompt and business logic instructions.


---

#### **Conclusion**

The prompt is the foundation of any interaction with an LLM. Its structure and processing determine the model’s behavior and the security of the application. By dissecting the internal structure of prompts, we gain insights into how LLMs function and where vulnerabilities lie. In the next chapter, we will explore specific techniques attackers use to exploit these vulnerabilities through prompt injections.