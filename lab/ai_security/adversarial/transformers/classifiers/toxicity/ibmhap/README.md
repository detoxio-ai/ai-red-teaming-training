# Adversarial attacks on NLP

Attacks expose how tiny, human-plausible edits (typos, synonyms, paraphrases) can flip model predictions. They’re great for stress-testing safety classifiers and measuring **robust accuracy**. ([textattack.readthedocs.io][1])

---

## 0) Quick Start (CLI)

**Create & activate an env (with `uv`)**

```bash
uv venv .venv
source .venv/bin/activate
uv sync
```

> Assumes your `pyproject.toml` (or requirements) already includes `textattack`, `transformers`, `datasets`, and a PyTorch build that matches your system.

**NLTK data (one-time)**

```bash
# assuming your script exists; e.g., ./setup_nltk.sh or ./nltk_setup.sh
./setup_nltk.sh
```

**Run a first attack (character-level, no POS needed)**

```bash
textattack attack \
  --model-from-huggingface ibm-granite/granite-guardian-hap-38m \
  --dataset-from-huggingface tweet_eval^hate^test \
  --recipe deepwordbug \
  --num-examples 200 \
  --enable-advance-metrics
```

* Target: IBM Granite Guardian HAP-38M (binary toxicity). ([Hugging Face][2])
* Dataset: TweetEval “hate” (binary).
* Recipe: **DeepWordBug** (character noise), fast and NLTK-light. ([textattack.readthedocs.io][1])

---

## 1) More attacks (CLI)

Try a few distinct perturbation styles to build a robustness profile:

```bash
# Word-level synonym swaps (needs NLTK data)
textattack attack \
  --model-from-huggingface ibm-granite/granite-guardian-hap-38m \
  --dataset-from-huggingface tweet_eval^hate^test \
  --recipe textfooler \
  --num-examples 200 \
  --enable-advance-metrics

# Masked-LM guided edits (fluency-preserving)
textattack attack \
  --model-from-huggingface ibm-granite/granite-guardian-hap-38m \
  --dataset-from-huggingface tweet_eval^hate^test \
  --recipe bae \
  --num-examples 200

# Character-typo recipe
textattack attack \
  --model-from-huggingface ibm-granite/granite-guardian-hap-38m \
  --dataset-from-huggingface tweet_eval^offensive^test \
  --recipe pruthi \
  --num-examples 200
```

Pro tip: add `--query-budget 200 --log-summary-to-json results.json --log-to-csv results.csv` to standardize comparisons across runs. ([textattack.readthedocs.io][1])

---

## 2) Minimal Python (programmatic attack)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from textattack.models.wrappers import HuggingFaceModelWrapper
from textattack.attack_recipes import TextFoolerJin2019
from textattack.datasets import HuggingFaceDataset
from textattack.attacker import Attacker
from textattack.attack_args import AttackArgs

# Target guard model (binary toxicity)
name = "ibm-granite/granite-guardian-hap-38m"
model = AutoModelForSequenceClassification.from_pretrained(name)
tok = AutoTokenizer.from_pretrained(name)
wrapper = HuggingFaceModelWrapper(model, tok)  # makes it TextAttack-compatible

# Dataset: TweetEval hate (test split)
dataset = HuggingFaceDataset("tweet_eval", "hate", "test", input_columns=["text"])

# Attack recipe
attack = TextFoolerJin2019.build(wrapper)

# Run a small batch and log results
args = AttackArgs(num_examples=100,
                  query_budget=200,
                  log_to_csv="hap38m_textfooler.csv",
                  checkpoint_interval=50,
                  enable_advance_metrics=True)
Attacker(attack, dataset, args).attack_dataset()
```

This mirrors the CLI, but lets you cap query budgets, checkpoint, and script experiments. ([textattack.readthedocs.io][3])

---

## 3) Interpreting results (what to watch)

* **Accuracy under attack (robust accuracy):** higher is better.
* **Attack success rate (ASR):** lower is better.
* **% perturbed words / avg queries:** how invasive and costly the attack is.
  These are standard in TextAttack’s summaries and CSV/JSON logs. ([textattack.readthedocs.io][1])

---

## Further reading

* **What is an adversarial attack (NLP)?** Concepts, components (goal, constraints, transformation, search). ([textattack.readthedocs.io][1])
* **Intro notebook (transformations, constraints, recipes).** ([textattack.readthedocs.io][3])
* **Model card:** *ibm-granite/granite-guardian-hap-38m*. ([Hugging Face][2])

If you want, I can add a tiny “robustness sweep” script that runs multiple recipes/datasets and collates a single comparison table.

[1]: https://textattack.readthedocs.io/en/latest/1start/what_is_an_adversarial_attack.html "What is an adversarial attack in NLP? — TextAttack 0.3.10 documentation"
[2]: https://huggingface.co/ibm-granite/granite-guardian-hap-38m "ibm-granite/granite-guardian-hap-38m · Hugging Face"
[3]: https://textattack.readthedocs.io/en/latest/2notebook/1_Introduction_and_Transformations.html "The TextAttack ecosystem: search, transformations, and constraints — TextAttack 0.3.10 documentation"
