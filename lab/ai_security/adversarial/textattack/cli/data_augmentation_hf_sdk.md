# Load and Augment `walledai/AdvBench`

## Objective

* Load the Hugging Face dataset `walledai/AdvBench` (train split).
* Safely inspect the first 5 `prompt` entries (redacted on screen).
* Randomly select 10 rows, augment the `prompt` text, and save a CSV with columns: `prompt,modified_prompt`.
* Make it easy to try different augmentation recipes later.

---

## 1) Setup in `txt1`

```bash
mkdir -p "$HOME/workspace/txt1"
cd "$HOME/workspace/txt1"

uv venv .venv
source .venv/bin/activate

uv pip install "textattack[tensorflow]" datasets pandas
```

---

## 2) Load the dataset and inspect (redacted preview)

Create `advbench_inspect.py`:

```python
#!/usr/bin/env python3
"""
Load walledai/AdvBench (train) and safely preview the first 5 prompts.
We redact console output to avoid displaying hazardous instructions.
"""

from datasets import load_dataset

def redact(s: str, keep=12) -> str:
    s = s.replace("\n", " ")
    return (s[:keep] + "…") if len(s) > keep else s

def main():
    ds = load_dataset("walledai/AdvBench", split="train")
    assert "prompt" in ds.column_names, "Column 'prompt' missing"

    print("Dataset columns:", ds.column_names)
    print("Number of rows:", len(ds))
    print("\nFirst 5 prompts (redacted):")
    for i in range(min(5, len(ds))):
        print(f"{i+1:>2}: {redact(ds[i]['prompt'])}")

if __name__ == "__main__":
    main()
```

Run:

```bash
python advbench_inspect.py
```

Result: you’ll see dataset size/columns and a **redacted** preview of five prompts.

---

## 3) Augment 10 random prompts and write CSV

Create `advbench_augment.py`:

```python
#!/usr/bin/env python3
"""
Randomly sample 10 rows from AdvBench (train), augment 'prompt',
and write 'advbench_augmented.csv' with columns: prompt, modified_prompt.

Edit RECIPE to try different techniques.
"""

import random
import pandas as pd
from datasets import load_dataset

from textattack.augmentation import (
    WordNetAugmenter,      # synonym substitutions
    CharSwapAugmenter,     # character-level noise
    EmbeddingAugmenter,    # embedding-nearest neighbors
    EasyDataAugmenter,     # EDA (synonym/insert/swap/delete)
    CheckListAugmenter,    # rule-based perturbations
    CLAREAugmenter,        # contextual masked-LM edits (slower)
    BackTranslationAugmenter  # round-trip translation (slowest)
)

# ---------------- Configuration (edit here) ----------------
SEED = 42
N_SAMPLE = 10
RECIPE = "wordnet"  # options: wordnet, charswap, embedding, eda, checklist, clare, back-translation
OUTPUT_CSV = "advbench_augmented.csv"
# For token/char recipes:
PCT_WORDS_TO_SWAP = 0.10
TRANS_PER_EXAMPLE = 1
# ----------------------------------------------------------

def build_augmenter(name: str):
    name = name.lower()
    if name == "wordnet":
        return WordNetAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                                transformations_per_example=TRANS_PER_EXAMPLE)
    if name in ("charswap", "char-swap", "char_swap"):
        return CharSwapAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                                 transformations_per_example=TRANS_PER_EXAMPLE)
    if name == "embedding":
        return EmbeddingAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                                  transformations_per_example=TRANS_PER_EXAMPLE)
    if name == "eda":
        return EasyDataAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                                 transformations_per_example=TRANS_PER_EXAMPLE)
    if name == "checklist":
        return CheckListAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                                  transformations_per_example=TRANS_PER_EXAMPLE)
    if name == "clare":
        return CLAREAugmenter(pct_words_to_swap=PCT_WORDS_TO_SWAP,
                              transformations_per_example=TRANS_PER_EXAMPLE)
    if name in ("back-translation", "back_translation", "backtrans", "back_trans"):
        return BackTranslationAugmenter(transformations_per_example=TRANS_PER_EXAMPLE)
    raise ValueError("Unknown RECIPE.")

def main():
    random.seed(SEED)

    # Load dataset
    ds = load_dataset("walledai/AdvBench", split="train")
    if "prompt" not in ds.column_names:
        raise SystemExit("Column 'prompt' not found.")

    # Sample indices
    idxs = list(range(len(ds)))
    random.shuffle(idxs)
    idxs = idxs[:N_SAMPLE]

    augmenter = build_augmenter(RECIPE)

    rows = []
    for i in idxs:
        original = ds[i]["prompt"]
        try:
            gens = augmenter.augment(original)  # list[str]
        except Exception as e:
            # Skip problematic rows, continue
            print(f"[warn] augmentation failed for index {i}: {e}")
            continue
        modified = gens[0] if gens else original
        rows.append({"prompt": original, "modified_prompt": modified})

    df = pd.DataFrame(rows, columns=["prompt", "modified_prompt"])
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(df)} rows to {OUTPUT_CSV}. Handle this file securely (contains unredacted text).")

if __name__ == "__main__":
    main()
```

Run:

```bash
python advbench_augment.py
```

This will produce `advbench_augmented.csv` with 10 rows, each containing the original `prompt` and its augmented `modified_prompt`.

---

## 4) Suggestions: change recipes and parameters

* Change `RECIPE` in `advbench_augment.py` to try:

  * `wordnet` (synonyms; fast)
  * `charswap` (character-level noise; fast)
  * `embedding` (semantic neighbors; moderate)
  * `eda` (mixed simple ops; fast)
  * `checklist` (rule-based perturbations; fast)
  * `clare` (contextual edits; slower; may download models)
  * `back-translation` (round-trip translation; slowest; ignores `PCT_WORDS_TO_SWAP`)
* Tune:

  * `PCT_WORDS_TO_SWAP` (e.g., 0.05–0.2) for token/char recipes.
  * `TRANS_PER_EXAMPLE` to emit more than one variant per prompt.
  * `SEED` for reproducible sampling.

