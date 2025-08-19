#!/usr/bin/env bash
# setup_nltk.sh — download NLTK resources required by TextAttack recipes
# No pip installs here; just NLTK data.
set -euo pipefail

# Use existing NLTK_DATA if set; otherwise default to ~/nltk_data
NLTK_DATA_DIR="${NLTK_DATA:-$HOME/nltk_data}"
export NLTK_DATA="$NLTK_DATA_DIR"
mkdir -p "$NLTK_DATA_DIR"

python - <<'PY'
import os, sys
import nltk

path = os.environ.get("NLTK_DATA", os.path.expanduser("~/nltk_data"))
os.makedirs(path, exist_ok=True)
# Ensure this path is searched first
nltk.data.path = [path] + [p for p in nltk.data.path if p != path]

packages = [
    "averaged_perceptron_tagger_eng",  # new POS tagger name
    "averaged_perceptron_tagger",      # old POS tagger name (for compatibility)
    "punkt",                           # tokenizer
    "wordnet",                         # WordNet (synonym constraints/transformations)
    "omw-1.4",                         # WordNet multilingual data
    "stopwords",                       # Stopword list
    "universal_tagset"                 # tagset mapping used by some POS constraints
]

print(f"Downloading NLTK data to: {path}")
ok = True
for pkg in packages:
    try:
        print(f" - {pkg} ...", end="", flush=True)
        success = nltk.download(pkg, download_dir=path, quiet=True)
        print(" done" if success else " FAILED")
        ok = ok and bool(success)
    except Exception as e:
        print(f" FAILED ({e})")
        ok = False

# Quick sanity check: tokenization + POS tag
try:
    from nltk import pos_tag, word_tokenize
    tags = pos_tag(word_tokenize("The quick brown fox jumps over the lazy dog."))
    print("Sanity check OK. Sample tags:", tags[:4])
except Exception as e:
    print(f"[ERROR] Sanity check failed: {e}", file=sys.stderr)
    sys.exit(2)

print("NLTK data paths now:", nltk.data.path)
sys.exit(0 if ok else 1)
PY

echo
echo "Done. Export persisted for this session:"
echo "  export NLTK_DATA=\"$NLTK_DATA_DIR\""
echo
echo "To persist for future shells, add this to your shell profile (~/.bashrc or ~/.zshrc):"
echo "  export NLTK_DATA=\"$NLTK_DATA_DIR\""

