
# Text Data Augmentation with TextAttack (SDK)

## 1) Create a workspace and Python environment

```bash
# folder
mkdir -p "$HOME/workspace/txt1"
cd "$HOME/workspace/txt1"

# virtual environment
python -m venv .venv
source .venv/bin/activate
```

## 2) Install TextAttack with TensorFlow extras

```bash
pip install -U pip
pip install "textattack[tensorflow]" pandas
```

Notes

* The `tensorflow` extra enables certain augmentation pipelines and will emit CUDA/TensorFlow warnings if GPUs/drivers are present. These are usually harmless for augmentation.

Optional: silence TF logs during augmentation

```bash
export TF_CPP_MIN_LOG_LEVEL=2
```

## 3) Create a small example dataset

Create `examples.csv` with two columns `text,label`. For instance:

```csv
"text",label
"the rock is destined to be the 21st century's new conan...",1
"the gorgeously elaborate continuation of 'the lord of the rings'...",1
"take care of my cat offers a refreshingly different slice...",1
"a technically well-made suspenser...",0
"it's a mystery how the movie could be released...",0
```

## 4) Add a simple augmentation script (SDK, no args)

Create `aug_sdk_simple.py` with the following contents. You will only edit the CONFIG block to switch recipes or outputs.

```python
#!/usr/bin/env python3
"""
Simple TextAttack SDK data augmenter (no argparse).
- Edit the placeholders in CONFIG below.
- Requires: pip install 'textattack[tensorflow]' pandas
"""

import csv
import random
import sys
from typing import List

import pandas as pd
from textattack.augmentation import (
    EasyDataAugmenter,        # eda
    WordNetAugmenter,         # wordnet
    EmbeddingAugmenter,       # embedding
    CharSwapAugmenter,        # charswap
    CheckListAugmenter,       # checklist
    CLAREAugmenter,           # clare
    BackTranslationAugmenter  # back-translation
)

# =========================
# CONFIG — EDIT THESE
# =========================
CONFIG = {
    "INPUT_CSV": "examples.csv",
    "OUTPUT_CSV": "out_wordnet.csv",
    "TEXT_COLUMN": "text",
    "LABEL_COLUMN": "label",

    # Choose one: "eda", "wordnet", "embedding", "charswap", "checklist", "clare", "back-translation"
    "RECIPE": "wordnet",

    # Applies to token/char recipes (not back-translation)
    "PCT_WORDS_TO_SWAP": 0.10,

    # Transformations per example
    "TPE": 2,

    # If True, only augmented rows are saved; originals are omitted
    "EXCLUDE_ORIGINAL": True,

    # Reproducibility where supported
    "SEED": 42,
}
# =========================


def build_augmenter(recipe: str, pct: float, tpe: int, seed: int):
    random.seed(seed)
    r = recipe.lower().strip()

    if r == "eda":
        return EasyDataAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r == "wordnet":
        return WordNetAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r == "embedding":
        return EmbeddingAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r in ("charswap", "char-swap", "char_swap"):
        return CharSwapAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r == "checklist":
        return CheckListAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r == "clare":
        return CLAREAugmenter(pct_words_to_swap=pct, transformations_per_example=tpe)
    if r in ("back-translation", "back_translation", "backtrans", "back_trans"):
        return BackTranslationAugmenter(transformations_per_example=tpe)

    raise ValueError("Unknown recipe. Use: eda, wordnet, embedding, charswap, checklist, clare, back-translation")


def augment_rows(texts: List[str], augmenter, include_original: bool) -> List[str]:
    out = []
    for txt in texts:
        if not isinstance(txt, str):
            txt = str(txt)
        if include_original:
            out.append(txt)
        try:
            gens = augmenter.augment(txt)  # list[str]
        except KeyError as e:
            sys.stderr.write(f"[warn] Skipping due to KeyError: {e}\n")
            gens = []
        out.extend(gens)
    return out


def main():
    cfg = CONFIG

    # Read input
    df = pd.read_csv(cfg["INPUT_CSV"])
    if cfg["TEXT_COLUMN"] not in df.columns:
        raise SystemExit(f"Missing column: {cfg['TEXT_COLUMN']}")
    if cfg["LABEL_COLUMN"] not in df.columns:
        raise SystemExit(f"Missing column: {cfg['LABEL_COLUMN']}")

    texts = df[cfg["TEXT_COLUMN"]].astype(str).tolist()
    labels = df[cfg["LABEL_COLUMN"]].tolist()

    # Build augmenter
    augmenter = build_augmenter(
        recipe=cfg["RECIPE"],
        pct=cfg["PCT_WORDS_TO_SWAP"],
        tpe=cfg["TPE"],
        seed=cfg["SEED"],
    )

    # Augment and preserve labels
    augmented_texts = []
    augmented_labels = []
    for txt, lab in zip(texts, labels):
        rows = []
        if not cfg["EXCLUDE_ORIGINAL"]:
            rows.append(txt)
        try:
            rows.extend(augmenter.augment(txt))
        except KeyError as e:
            sys.stderr.write(f"[warn] CLARE/augment KeyError: {e}. Skipping.\n")

        for r in rows:
            augmented_texts.append(r)
            augmented_labels.append(lab)

    # Write output
    with open(cfg["OUTPUT_CSV"], "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([cfg["TEXT_COLUMN"], cfg["LABEL_COLUMN"]])
        for t, l in zip(augmented_texts, augmented_labels):
            writer.writerow([t, l])

    print(f"Wrote {len(augmented_texts)} rows to {cfg['OUTPUT_CSV']}")


if __name__ == "__main__":
    main()
```

## 5) Run the script

```bash
python aug_sdk_simple.py
```

This will read `examples.csv` and write `out_wordnet.csv` with augmented rows and copied labels.

## 6) Try different augmentation techniques

Edit `RECIPE` in the CONFIG block of `aug_sdk_simple.py` and re-run. Suggested values:

* `wordnet` (WordNet synonyms; what you already used)
* `embedding` (nearest-neighbor replacements in embedding space)
* `charswap` (character-level swaps/inserts/deletes)
* `eda` (Easy Data Augmentation: synonym replace/insert, random swap/delete)
* `checklist` (rule-based textual perturbations)
* `clare` (contextual masked-LM edits; slower; may download models)
* `back-translation` (round-trip translation; slower; ignores `PCT_WORDS_TO_SWAP`)


## 7) Inspect the results

```bash
head -n 5 out_wordnet.csv
```