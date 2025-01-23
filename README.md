# **AI Red Teaming**

This repository contains a structured and detailed guide on **AI Red Teaming**, exploring its history, risks, techniques, and architectural principles. The book provides both theoretical and practical insights into the red teaming of AI systems, covering foundational knowledge and hands-on demonstrations.

![image](https://github.com/user-attachments/assets/dc0494ae-5297-4aa4-bac7-5ac05f5b72af)

---

## **Introduction**

AI Red Teaming is a structured process designed to evaluate the security, robustness, and ethical alignment of artificial intelligence systems. This book is an effort to guide practitioners, researchers, and enthusiasts in understanding and implementing AI red teaming strategies effectively.

Through this repository, you will:
- Learn the history and evolution of AI risks and failures.
- Understand the taxonomy of AI attacks and adversarial techniques.
- Dive into the inner workings of large language models (LLMs), including transformers, tokenization, and hyperparameters.
- Gain hands-on experience with tools and techniques such as adversarial testing and jailbreaking.

---

## **Structure**

The content is divided into chapters across four main sections: **AI Red Teaming**, **LLM Architecture**, **Prompt Injections**, and **LLM Training**. Below is the structure with direct links to the files.

### **1. Introduction to AI Attacks**
- [1.1 History of AI Risks](content/1_intro_ai_red_teaming/1_1_history_of_ai_risks.md)
- [1.2 AI Risks](content/1_intro_ai_red_teaming/1_2_ai_risks.md)
- [1.3 What is AI Red Teaming?](content/1_intro_ai_red_teaming/1_3_ai_red_teaming.md)
- [1.4 AI Attacks Taxonomy (Part 1)](content/1_intro_ai_red_teaming/1_4_ai_attacks_taxonomy_part_1.md)
- [1.5 AI Attacks Taxonomy (Part 2)](content/1_intro_ai_red_teaming/1_5_ai_attacks_taxonomy_part_2.md)
- [1.6 Jailbreaking Demo](content/1_intro_ai_red_teaming/1_6_jailbreaking_demo.md)

### **2. LLM Architecture for Security Professionals**
- [2.1 History of LLMs](content/2_llm_architecture/2_1_history_of_llms.md)
- [2.2 Tokenization](content/2_llm_architecture/2_2_tokenization.md)
- [2.3 Self-Attention](content/2_llm_architecture/2_3_self_attention.md)
- [2.4 Transformer Architecture](content/2_llm_architecture/2_4_transformer.md)
- [2.5 Hyperparameters](content/2_llm_architecture/2_5_hyperparameters.md)
- [2.6 LLM Comparisons](content/2_llm_architecture/2_6_llm_comparisons.md)

### **3. Prompt Injections**
- [3.1 Intro to Prompt Injections](content/3_prompt_injections/3_1_intro_prompt_injections.md)
- [3.1.1 Real-life Prompt Injection Examples](content/3_prompt_injections/3_1_1_realife_prompt_injection_examples.md)
- [3.2 Anatomy of a Prompt](content/3_prompt_injections/3_2_anatomy_of_a_prompt.md)
- [3.3 Craft a Prompt Injection Prompt](content/3_prompt_injections/3_3_craft_a_prompt_injection_prompt.md)
- [3.4 Basics of Prompt Injection Techniques](content/3_prompt_injections/3_4_basics_of_prompt_injection_techniques.md)
- [3.5 Intermediate Prompt Injection Techniques](content/3_prompt_injections/3_5_intermediate_prompt_injection_techniques.md)
- [3.7 Try Prompt Injections on Medusa Pokebot](content/3_prompt_injections/3_7_try_prompt_injections_on_medusa_pokebot.md)
- [3.8 Advanced Prompt Injections](content/3_prompt_injections/3_8_advance_prompt_injections.md)

### **4. LLM Training**
- [4.1 Inference Advanced Parameters](content/4_llm_training/4_1_inference_advance_params.md)
- [4.2 Foundation Model Training](content/4_llm_training/4_2_foundation_model_training.md)
- [4.3 Fine-Tuning LLMs](content/4_llm_training/4_3_finetuing_llms.md)
- [4.4 Retrieval-Augmented Generation (RAG)](content/4_llm_training/4_4_rag.md)

---

## **Getting Started**

To begin exploring the content:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository-name.git
   ```
2. Navigate through the chapters using the links provided in the **Structure** section.

---

## **How to Contribute**

Contributions are highly encouraged! Here's how you can get involved:

### 1. **Submit a Ticket**
   - Found a bug, typo, or inconsistency?  
     You can contribute by creating a ticket or an issue.  
     To do so:
     1. Go to the **Issues** tab in this repository.
     2. Click on **New Issue**.
     3. Fill in the issue template with relevant details.
     4. Submit your ticket to notify maintainers of the problem or suggestion.

   This is an excellent way to contribute even if you're not comfortable with coding or writing directly in the repository.

### 2. **Fork the Repository**
   - Click the **Fork** button at the top right of this repository to create your own copy.

### 3. **Clone Your Fork**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/ai-red-teaming.git
     ```

### 4. **Create a Branch**
   - Create a new branch to work on a specific feature or fix:
     ```bash
     git checkout -b feature-or-fix-name
     ```

### 5. **Make Changes**
   - Add your contributions or edits to the appropriate file(s).

### 6. **Test Your Changes**
   - Ensure that your changes are accurate and do not introduce issues.

### 7. **Commit Changes**
   - Commit your changes with a descriptive message:
     ```bash
     git add .
     git commit -m "Add detailed description of your changes"
     ```

### 8. **Push to Your Fork**
   - Push your changes to your forked repository:
     ```bash
     git push origin feature-or-fix-name
     ```

### 9. **Create a Pull Request**
   - Go to the original repository and create a Pull Request (PR) from your forked branch. Describe your changes and why they should be merged.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
