# Prompt Templates YAML Guide  
**For Red-Teaming LangChain Hub Prompt Templates**

This guide explains how to define, load, and test prompts using YAML configuration files. It is especially useful when red-teaming prompt templates from [LangChain Hub](https://smith.langchain.com/hub), enabling you to validate robustness, edge cases, and failure modes in structured, repeatable ways.

---

## Overview: Prompt Templates on LangChain Hub

LangChain Hub provides a growing library of prompt templates for LLM applications. These templates are modular, reusable, and cover use cases such as:

- Retrieval-Augmented Generation (RAG)
- Chatbots and Assistants
- Document Q&A
- Summarization
- Classification and Extraction

For example, the [`rlm/rag-prompt`](https://smith.langchain.com/hub/rlm/rag-prompt) template is widely used for question answering with context retrieval:

```
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
```

### How to Load a Prompt Template from LangChain Hub

```python
# Ensure you have a LANGSMITH_API_KEY from Settings > API Keys
from langsmith import Client

client = Client(api_key=LANGSMITH_API_KEY)
prompt = client.pull_prompt("rlm/rag-prompt", include_model=True)
```

This pulls the template and its metadata, which can then be used in red-team evaluations, model fine-tuning, or prompt chaining setups.

---

## Generate and Test Prompts Using CLI

Use the `dtx` CLI tool to quickly build, test, and red-team prompt templates interactively.

### Steps to Launch an Interactive Test Template

1. Run:

   ```bash
   dtx redteam quick
   ```

2. You’ll see:

   ```
   2025-04-19 08:32:38 | INFO     | dtx.core.logging:_log:84 - Loading env from local env
   Environment check passed.
   ╭──────────────── Agent Builder ────────────────╮
   │ Let's build your agent interactively!        │
   │ Choose from web models or template repos.    │
   ╰──────────────────────────────────────────────╯
         Agent Options      
   ┏━━━━━┳━━━━━━━━━━━━━━━━━┓
   ┃ No. ┃ Option          ┃
   ┡━━━━━╇━━━━━━━━━━━━━━━━━┩
   │  1  │ HTTP Provider   │
   ├─────┼─────────────────┤
   │  2  │ Gradio Provider │
   ├─────┼─────────────────┤
   │  3  │ LangHub Prompts │
   └─────┴─────────────────┘
   Enter the number of the agent type you want to use [1/2/3] (3): 
   ```

3. Select option `3` to test a LangHub-based prompt interactively.

This will create a redteam-ready prompt agent configured with a chosen template, ready for input testing and evaluation.

---


## YAML Section in the Scope or Plan file

```yaml
prompts:
  - id: langhub
    config:
      full_name: rlm/rag-prompt
      prompt:
        metadata:
          id: "some-uuid"
          name: rag-prompt
          owner: rlm
          description: >
            This is a prompt for retrieval-augmented generation (RAG).
            It is useful for chatbots, question answering, or any task
            that involves passing context to a language model.
          tags:
            - ChatPromptTemplate
            - QA over documents
            - English
          full_name: rlm/rag-prompt

        conversation:
          turns:
            - role: USER
              message: |
                You are an assistant for question-answering tasks.
                Use the following retrieved context to answer the question.
                If you don't know the answer, say that you don't know.
                Keep the answer concise and under three sentences.

                Question: {question}
                Context: {context}
                Answer:

        input_variables:
          - context
          - question

      params:
        - name: context
          value: "{{file://data/sample_context.txt}}"

        - name: question
          value: |
            Let's make this interesting!
            The user asked: {{prompt}}

providers:
  - id: openai
    config:
      model: gpt-4o
      task: generation
      params: null
      endpoint: https://api.openai.com/v1
```

---

## Concepts

### 1. Placeholders in Prompts

Use curly braces for template variables:

```yaml
Question: {question}
Context: {context}
Answer:
```

These correspond to the variable names in the `input_variables` and `params` sections.

---

### 2. Parameters Section (`params`)

The `params` block is how you inject values into placeholders.

```yaml
params:
  - name: context
    value: "{{file://data/sample_context.txt}}"

  - name: question
    value: |
      Let's make this interesting!
      The user asked: {{prompt}}
```

---

### 3. Meta Variables in Double Braces

Meta expressions like `{{prompt}}` are resolved at runtime. This supports:

| Syntax | Description |
|--------|-------------|
| `{{prompt}}` | Current user input |
| `{{file://path}}` | Load content from a file |
| `{{env:VAR}}` | (Future) Environment variable support |

---

### 4. Multi-line Block Values

Use `|` for multi-line strings:

```yaml
- name: question
  value: |
    Please answer the following carefully:
    {{prompt}}
```

This is recommended for long or complex prompt fragments.

---

## Runtime Flow

1. Load YAML configuration.
2. Resolve all meta values inside `{{ }}`.
3. Replace all `{placeholders}` in the prompt with resolved values.
4. Construct final prompt text.
5. Send to the model via provider (e.g., OpenAI, Anthropic).

---

## Sample Output Prompt

Input:

- `prompt`: *What is the boiling point of water?*
- `sample_context.txt`: *Water boils at 100 degrees Celsius.*

Output:

```
You are an assistant for question-answering tasks.
Use the following retrieved context to answer the question.
If you don't know the answer, say that you don't know.
Keep the answer concise and under three sentences.

Question: Let's make this interesting!
The user asked: What is the boiling point of water?
Context: Water boils at 100 degrees Celsius.
Answer:
```

---

## Best Practices

- Use `{{ }}` for dynamic expressions and `{}` for placeholder injection.
- Always validate file paths and external references before running.
- Keep prompts under a reasonable token length for testing.
- Red-team prompts with adversarial questions, ambiguous phrasing, and empty context to explore failure modes.
- Use `dtx redteam quick` to simulate and inspect prompt behavior locally.

---

## Advanced Capabilities (Optional)

- Define multiple prompt templates in a single YAML file
- Enable fallback values (e.g., `{{prompt | "default"}}`) in future versions
- Integrate environment values (`{{env:VAR}}`) for secrets and config injection

---
