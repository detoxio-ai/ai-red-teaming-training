## Red‑Teaming a Hugging Face Space (Gradio API) with `dtx`

Use this guide to red-team **a Hugging Face Space or Gradio-hosted model endpoint** using `dtx redteam quick`.

---

### ⚡ Step 1: Launch Quick Interactive Setup

Start the interactive CLI:

```bash
dtx redteam quick
```

You'll see a guided, menu-based configuration flow.

---

### 🧩 Step 2: Select Gradio as the Agent Type

You’ll be asked to choose an agent type:

```
Enter the number of the agent type you want to use [1/2/3/4] (4): 2
```

✅ **Choose option `2` – Gradio Provider**

---

### 🌐 Step 3: Provide the API Endpoint

Now enter your Hugging Face Space or Gradio endpoint:

```bash
http://<YOUR_HF_SPACE_URL>/
```

Example:

```bash
http://104.154.231.188:17860/
```

This should be the base URL of your running Gradio app.

---

### 🔌 Step 4: Configure the API Path

The CLI will list available endpoints:

```
Available APIs
1. /update_system_prompt
2. /chatbot_response
3. /chatbot_response_1
```

✅ Choose the correct endpoint for conversation (e.g. `/chatbot_response`)
Enter:

```
2
```

---

### 🎛 Step 5: Configure API Parameters

You'll be prompted to define how inputs will be mapped:

| Field                     | Set value / leave default                          |
| ------------------------- | -------------------------------------------------- |
| `user_input`              | `{{prompt}}` (auto-filled)                         |
| `chat_history`            | Leave empty (`[]`)                                 |
| `selected_role`           | Optional, use default or one of the dropdown roles |
| `security_toggle`         | `True`                                             |
| `jailbreak_toggle`        | `True`                                             |
| `prompt_injection_toggle` | `False`                                            |
| `hask_toggle`             | `False`                                            |

These settings determine how test prompts are routed into your app.

Once finished, the provider will be generated and ready.

---

### 🧠 Step 6: Select a Dataset for Prompt Generation

Choose a dataset for adversarial prompts:

```
Enter the number of the dataset you want to use [1–15] (1): 7
```

✅ Recommended:

* `7` = `HF_SAFEMTDATA` → Multi-turn jailbreak test prompts
* Others: `HF_JAILBREAKBENCH`, `HF_FLIPGUARDDATA`, `HF_BEAVERTAILS`

---

### ✍️ Step 7: Customize Prompt Counts

Set how many prompts to include:

```
Enter max number of prompts to generate (20): 
Enter number of prompts per risk category (5): 
```

Adjust based on how long you're willing to run the test.

---

### 💾 Step 8: Save Plan & Scope

You'll be prompted to save your plan and scope:

```
Enter filename to save the RedTeam Plan (redteam_plan.yml): 
Enter filename to save the RedTeam Scope (redteam_scope.yml): 
```

Example:

```bash
redteam_plan.yml
redteam_scope.yml
```

---

### 🚀 Step 9: Run the RedTeam Evaluation

After generating the plan, the CLI asks:

```
Do you want to run the RedTeam tests now? (yes/no): yes
```

Then:

```
Enter the filename to save the RedTeam test results (report.yml):
```

Example:

```bash
gradio_report.yml
```

Once done, you’ll have YAML test results saved with model responses to adversarial prompts.

---

### 📊 Optional: Export an HTML Report

If you'd like to generate a viewer-friendly report:

```bash
dtx redteam run \
  --plan_file redteam_plan.yml \
  --agent gradio \
  --url http://104.154.231.188:17860/ \
  --html ./shared/gradio_report.html \
  -o
```
