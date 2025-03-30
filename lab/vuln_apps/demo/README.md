# Quick Start Guide

## Setup Instructions

### 1. Navigate to the `demo` Folder

Before installing dependencies, move to the `demo` folder:

```sh
cd demo
```

### 2. Copy `.env.template` to `.env` and Update `OPENAI_API_KEY`

```sh
cp .env.template .env
```

Set your OpenAI API Key to access the model.

### 3. Install Dependencies Using Poetry

```sh
poetry install
```

You can install Poetry on your system if not installed:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 4. Activate Poetry Shell (to activate environment)

```sh
poetry shell
```

You can install Poetry Shell on your system if not installed:

```sh
poetry self add poetry-plugin-shell
```

### 5. Run Application Using Gradio

```sh
gradio main.py
```

You can access the chatbot UI at: `http://localhost:7860`

---

## How It Works 🛡️

1. The chatbot receives a user's input.
2. If **Enable Security Checks** is checked (by default checked), additional security checks are performed:
   - If **Jailbreak Detection** is enabled (by default checked), it checks for jailbreak attempts.
   - If **Prompt Injection Detection** is enabled (by default unchecked), it scans for prompt injection threats.
3. If security checks pass, OpenAI processes the query and returns a response.
4. The response is displayed in an easy-to-use chat interface.

---

## Security Check Behavior 🔄

| Enable Security Checks | Jailbreak Detection | Prompt Injection Detection | Behavior |
|------------------------|--------------------|---------------------------|----------|
| ✅ Checked            | ✅ Checked         | ❌ Unchecked               | Default state when enabled |
| ✅ Checked            | ✅ Checked         | ✅ Checked                 | Both checks enabled |
| ✅ Checked            | ❌ Unchecked       | ✅ Checked                 | Only prompt injection check enabled |
| ❌ Unchecked          | ❌ Hidden          | ❌ Hidden                  | Security checks disabled, states hidden |
| ✅ Checked → ❌ Unchecked | ❌ Unchecked  | ❌ Unchecked               | Security checks auto-disabled, states hidden |

*When Security checks are disabled, the states will be hidden.*  
*When both states are unchecked, Security checks will be disabled and states will be hidden.*  
*The previous state of checkboxes is reset to their default states when re-enabling security mode.*  

---

## API Reference 📝

### Endpoint:

The application runs locally at:

```
http://localhost:7860
```

### Inputs:

| Parameter                | Type      | Description                                  |
| ------------------------ | --------- | -------------------------------------------- |
| `user_input`             | `string`  | The message typed by the user.               |
| `security_toggle`        | `boolean` | Enables/disables security checks.            |
| `jailbreak_check`        | `boolean` | Enables/disables jailbreak detection.        |
| `prompt_injection_check` | `boolean` | Enables/disables prompt injection detection. |

### Outputs:

| Response       | Description                                                           |
| -------------- | --------------------------------------------------------------------- |
| `chat_history` | A structured chat response, including user messages and AI responses. |

---

