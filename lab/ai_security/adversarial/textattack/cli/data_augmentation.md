# Data Augmentation with TextAttack (CLI)

## Create a working folder and a small dataset

```bash
mkdir -p "$HOME/workspace/txt1"
cd "$HOME/workspace/txt1"

# optional: create & activate a local venv
uv  venv .venv
source .venv/bin/activate

# install textattack
uv pip install textattack
```

Create `examples.csv` with two columns `text,label` (as you did). Example:

```csv
"text",label
"the rock is destined to be the 21st century's new conan...", 1
"the gorgeously elaborate continuation of 'the lord of the rings'...", 1
"take care of my cat offers a refreshingly different slice...", 1
"a technically well-made suspenser...", 0
"it's a mystery how the movie could be released...", 0
```

## Run augmentation (baseline example)

```bash
textattack augment \
  --input-csv examples.csv \
  --output-csv output.csv \
  --input-column text \
  --recipe wordnet \
  --pct-words-to-swap .1 \
  --transformations-per-example 2 \
  --exclude-original
```

Notes:

* `--pct-words-to-swap`: fraction of tokens to replace per example.
* `--transformations-per-example`: how many augmented variants per row.
* `--exclude-original`: only augmented rows in the output file.
* Add `--random-seed 42` for reproducibility.

Your run produced `output.csv` with 10 rows (2 per original line).

## Try other recipes quickly

Replace `--recipe ...` with any of the following and keep the rest of the flags the same. Change output filename per recipe.

```bash
# WordNet synonym swap (what you used)
textattack augment --input-csv examples.csv --output-csv out_wordnet.csv \
  --input-column text --recipe wordnet --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# Embedding-space nearest neighbors
textattack augment --input-csv examples.csv --output-csv out_embedding.csv \
  --input-column text --recipe embedding --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# Character-level swaps/inserts/deletes
textattack augment --input-csv examples.csv --output-csv out_charswap.csv \
  --input-column text --recipe charswap --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# EDA (synonym replace, insert, swap, delete)
textattack augment --input-csv examples.csv --output-csv out_eda.csv \
  --input-column text --recipe eda --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# Checklist-style perturbations (e.g., contractions, typos, punctuation)
textattack augment --input-csv examples.csv --output-csv out_checklist.csv \
  --input-column text --recipe checklist --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# CLARE (contextual masked LM edits; slower, higher quality)
textattack augment --input-csv examples.csv --output-csv out_clare.csv \
  --input-column text --recipe clare --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original

# Back-translation (may download models; slower)
textattack augment --input-csv examples.csv --output-csv out_backtrans.csv \
  --input-column text --recipe back-translation --pct-words-to-swap .1 \
  --transformations-per-example 2 --exclude-original
```

## Other Techniques


### **1. `eda` (Easy Data Augmentation)**

This is a foundational recipe that combines four simple, computationally cheap heuristics. For a given sentence, it randomly chooses one of the following operations:
* **Synonym Replacement:** Replaces some words with their synonyms.
* **Random Insertion:** Adds a random word's synonym into the sentence.
* **Random Swap:** Swaps the positions of two random words.
* **Random Deletion:** Removes a random word.

**Best for:** A quick and effective baseline for increasing data diversity and improving model generalization with minimal effort.

### **2. `wordnet`**

This technique focuses purely on synonym replacement using the WordNet lexical database. It identifies words (nouns, verbs, adjectives, adverbs) in a sentence and substitutes them with synonyms from WordNet.

**Best for:** Increasing the lexical variety of your dataset, teaching the model that different words can carry the same meaning. It is less context-aware than newer methods.

### **3. `embedding`**

This is a more sophisticated form of word replacement. It uses pre-trained word embeddings (like GloVe) to find replacements. Instead of strict synonyms, it finds words that are semantically close in the vector space, leading to more contextually appropriate substitutions than `wordnet`.

**Best for:** Generating plausible and contextually relevant word replacements that maintain the sentence's natural flow and meaning.

### **4. `char-swap` (Character-level Perturbations)**

This technique operates on the characters within words, not the words themselves. It introduces small errors by randomly swapping, inserting, deleting, or substituting characters.

**Best for:** Making models robust against common typos and misspellings, which is crucial for applications that handle raw user input (e.g., search engines, chatbots, social media analysis).

### **5. `checklist`**

Inspired by behavioral testing of NLP models, this is a more targeted augmentation method. Instead of random changes, it applies specific perturbations like changing names, locations, numbers, or adding negation to test if the model's logic is sound.

**Best for:** Probing for model biases and improving robustness on specific linguistic phenomena, rather than just general diversification.

### **6. `clare`**

This is a powerful, context-aware recipe that uses a pre-trained masked language model (like BERT or RoBERTa). It intelligently modifies sentences by asking the model to **replace**, **insert**, or **merge** words based on the full context of the sentence, resulting in very fluent and high-quality augmentations.

**Best for:** Creating highly natural and grammatically correct augmented data when quality is more important than computational speed.

### **7. `back-translation`**

This technique leverages machine translation services. It translates text from the source language (e.g., English) to an intermediate language (e.g., German) and then translates it back to the source language. This process effectively paraphrases the original sentence, often changing its structure and word choice while preserving its meaning.
