# Features and Options

This document outlines the key CLI commands you can use to explore available tactics, datasets, plugins, and providers in the `dtx` interface.

> Note: If you are using Docker, you can simply replace `dtx` with `ddtx`.

---

## Tactics

List all available tactics that can be applied for model evaluation or adversarial testing.

```bash
dtx tactics list
```

Each tactic includes:
- **Name** — the identifier used in test plans.
- **Description** — explains how the tactic manipulates prompts or attacks models.

Example tactic:
- `flip_attack`: Flips characters or words in a prompt to bypass filters while remaining interpretable to the model.

---

## Datasets

Explore curated prompt datasets for evaluating language models.

```bash
dtx datasets list
```

Datasets include themes such as:
- Jailbreak testing
- Misinformation
- Toxicity detection
- AI safety benchmarks

Example datasets:
- `HF_JAILBREAKBENCH`
- `HF_FLIPGUARDDATA`
- `HF_AISAFETY`
- `STRINGRAY` (default, no external dependencies)

---

## Plugins

List all available plugins used for evaluating model outputs across different risk categories.

```bash
dtx plugins list
```

Plugins cover evaluation domains such as:
- Toxicity detection
- Misinformation identification
- Information hazards
- Malicious use
- Defense bypass
- Hallucinations and overconfidence

Plugin format:
```
<category>:<subcategory>:<specific check>
```

Example:
- `toxicity:hate_speech:discrimination`
- `misinformation:climate:denialism`

---

## Providers

Use providers to generate completions or integrate with various LLM systems.

> Currently, the `providers` command supports the `generate` subcommand.

Check available options:

```bash
dtx providers generate --help
```

You can use this to:
- Spin up HTTP providers
- Generate test completions
- Interface with services like Ollama, OpenAI, and others

---

## Summary

| Command | Description |
|---------|-------------|
| `dtx tactics list` | List all available adversarial tactics |
| `dtx datasets list` | Explore prompt datasets for testing |
| `dtx plugins list` | List plugins for output evaluation |
| `dtx providers generate --help` | Get help on generating completions with providers |

For Docker users, simply replace `dtx` with `ddtx` in the above commands.

