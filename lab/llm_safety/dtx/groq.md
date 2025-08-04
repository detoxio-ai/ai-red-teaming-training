## 🚀 Tutorial: Red‑Teaming AI Models with `dtx`

### 🔧 Step 1: Overview & Prerequisites

To evaluate Groq‑hosted models using adversarial or safety-focused tests, you’ll use the `dtx redteam run` command. You’ll need:

* `dtx` installed in your Python environment
* Access to Groq (e.g. via `GROQ_API_KEY`)
* Ability to view generated HTML reports

---

### 🛠 Step 2: Running a Test on a Sample Model

Test **DeepSeek's 70B distilled LLaMA model** using the AirBench dataset with the following:

```bash
dtx redteam run --agent groq --url deepseek-r1-distill-llama-70b -o --html ./shared/groq_report.html --dataset airbench
```

* `--agent groq`: Use Groq as the backend
* `--url`: Target the specified model
* `--dataset`: Select AirBench for red-teaming prompts
* `-o` and `--html`: Output an HTML report

To view the results:

```
http://<YOUR_IP_ADDRESS>/groq_report.html
```

---

### 📋 Step 3: List of Available Groq Models

Replace the model ID in `--url` with any of the following:

#### ✅ Production Models

* `gemma2-9b-it`
* `llama-3.1-8b-instant`
* `llama-3.3-70b-versatile`
* `meta-llama/llama-guard-4-12b`
* `whisper-large-v3`
* `whisper-large-v3-turbo`

#### 🔍 Preview Models

* `deepseek-r1-distill-llama-70b`
* `meta-llama/llama-4-maverick-17b-128e-instruct`
* `meta-llama/llama-4-scout-17b-16e-instruct`
* `meta-llama/llama-prompt-guard-2-22m`
* `meta-llama/llama-prompt-guard-2-86m`
* `moonshotai/kimi-k2-instruct`
* `playai-tts`
* `playai-tts-arabic`
* `qwen/qwen3-32b`

#### 🧪 Tool-Use Preview Models

* `llama3-groq-70b-tool-use-preview`
* `llama3-groq-8b-tool-use-preview`

📖 Full list at: [https://console.groq.com/docs/models](https://console.groq.com/docs/models)

---

### 🔁 Step 4: Reusable Command Template

To test any Groq-hosted model, run:

```bash
dtx redteam run \
  --agent groq \
  --url <MODEL_ID> \
  -o \
  --html ./shared/<MODEL_ID>_report.html \
  --dataset airbench
```

Replace `<MODEL_ID>` with any model from the list above.

---

### 🧾 Summary Table

| Step        | What to do                                                                 |
| ----------- | -------------------------------------------------------------------------- |
| 1. Setup    | Install `dtx`, set up `GROQ_API_KEY`, prepare a browser to open the report |
| 2. Run Test | Use `dtx redteam run --agent groq --url MODEL_ID ...`                      |
| 3. View     | Open the report at `http://<your_ip>/path_to_report.html`                  |
| 4. Iterate  | Swap in different `--url` model IDs to compare performance                 |

---

### 🌐 Official Reference

* Full model list and documentation:
  [https://console.groq.com/docs/models](https://console.groq.com/docs/models)
