## 🧪  Targeted Red-Teaming of GPT-4o using `dtx`

This tutorial demonstrates **plugin-filtered**, **framework-specific**, and **dataset-controlled** evaluations using OpenAI’s GPT-4o model.

---

### 🔧 Step 1: Basic RedTeam Run with GPT‑4o

Here’s a simple, fast way to test GPT‑4o with AirBench:

```bash
dtx redteam run \
  --agent openai \
  --url gpt-4o \
  -o \
  --html ./shared/openai_report.html \
  --dataset airbench
```

This command:

* Uses OpenAI as the backend
* Targets `gpt-4o`
* Evaluates with `airbench` dataset
* Outputs an HTML report to `./shared/openai_report.html`

---

### 🛠 Step 2: Scope Specific Plugins (e.g. Hallucination & Toxicity)

Focus your evaluation by selecting only a subset of plugins:

```bash
dtx redteam scope \
  --plugin hallucination \
  --plugin "^toxicity" \
  "Scope for hallucination and toxicity checks" \
  redteam_scope.yml
```

✅ This creates a filtered scope file: `redteam_scope.yml`, including only plugins:

* Related to hallucination
* Starting with `toxicity` (e.g., hate speech, slurs, harassment)

---

### 📋 Step 3: Generate a Full RedTeam Plan

Create a detailed plan using the scope and dataset:

```bash
dtx redteam plan \
  redteam_scope.yml \
  redteam_plan.yml \
  --dataset HF_JAILBREAKBENCH \
  --max_prompts 20 \
  --max_prompts_per_plugin 5 \
  --max_goals_per_plugin 3
```

✅ This:

* Reads your filtered plugin scope
* Sets dataset to **HF\_JAILBREAKBENCH**
* Caps prompts and goals to manageable limits
* Outputs: `redteam_plan.yml`

---

### 🚀 Step 4: Run the Test Plan

Now run the plan with OpenAI’s GPT‑4o:

```bash
dtx redteam run \
  --plan_file redteam_plan.yml \
  --agent openai \
  --url gpt-4o \
  --samples 2 \
  --output \
  --html ./shared/openai_scope_report.html
```

✅ Notes:

* No need to re-pass `--plugin` — the plan includes them
* You can adjust `--samples` to test more generations per prompt

---

### ⚡ Bonus: Do It All in One Step

No pre-built scope or plan needed—`dtx` can handle it dynamically:

```bash
dtx redteam run \
  --agent openai \
  --url gpt-4o \
  --dataset HF_JAILBREAKBENCH \
  --plugin hallucination \
  --plugin "^toxicity" \
  --samples 2 \
  --output \
  --html ./shared/openai_dynamic_report.html
```

✅ This:

* Builds scope on-the-fly
* Generates a temporary plan
* Runs red-teaming against GPT‑4o
* Outputs results to `openai_dynamic_report.html`

---

### 📚 Plugin Filtering – What You Can Match

| Type    | Example                      | Matches                             |
| ------- | ---------------------------- | ----------------------------------- |
| Full ID | `toxicity:hate_speech:slurs` | Exact plugin ID                     |
| Keyword | `hallucination`              | Any plugin tagged with that keyword |
| Regex   | `^toxicity`                  | Plugins starting with "toxicity"    |

Use multiple `--plugin` flags to include multiple checks.

---

### 📁 Output Formats

| Format | Flag                  |
| ------ | --------------------- |
| YAML   | `--yml results.yml`   |
| JSON   | `--json results.json` |
| HTML   | `--html results.html` |

Always include `-o` or `--output` to enable saving reports.

---
