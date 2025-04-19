# Overview: Prompt Datasets

The `dtx` red teaming framework includes a curated set of **prompt datasets** designed to test and evaluate LLM behavior under adversarial, risky, or sensitive conditions. These datasets serve as **generators**, producing prompts that are passed to AI models (targets) for evaluation.

Each dataset targets a specific type of risk: jailbreaks, misinformation, manipulation, toxicity, or safety compliance.

---

## Dataset Descriptions

| Dataset Name        | Description |
|---------------------|-------------|
| **STRINGRAY**        | Prompts derived from [Garak](https://github.com/leondz/garak) Scanner Signatures. Focuses on known red teaming patterns and prompt anomalies. |
| **STARGAZER**        | Generates adversarial prompts using OpenAI models. Useful for zero-day or emergent exploit discovery. |
| **HF_BEAVERTAILS**   | Contains prompts designed to test behavioral manipulation and safety bypasses. Focused on instruction-following risks. |
| **HF_HACKAPROMPT**   | A Hugging Face dataset curated for jailbreak and prompt injection scenarios. Often includes known exploits. |
| **HF_JAILBREAKBENCH**| A benchmark suite for systematically testing jailbreak vulnerabilities across LLMs. |
| **HF_SAFEMTDATA**    | Focuses on **multi-turn** prompt scenarios. Tests whether LLMs become unsafe in extended conversations. |
| **HF_FLIPGUARDDATA** | Designed for **character-level adversarial prompts**, like emoji-swaps or homoglyph attacks. |
| **HF_JAILBREAKV**    | An updated collection of jailbreak prompts combining legacy and recent exploit cases. |
| **HF_LMSYS**         | Extracted from real-world chat logs (LMSYS), used to evaluate contextual vulnerabilities and safety drift. |
| **HF_AISAFETY**      | Created by AI Safety Lab, this dataset contains prompts targeting misinformation, toxicity, and general unsafe behavior. |
| **HF_AIRBENCH**      | A large-scale benchmark (AIR-Bench 2024) covering a broad range of AI risks: security, privacy, manipulation, harmful content, and disinformation. Ideal for comprehensive red teaming. |

---

## How to Use a Dataset

To view the available datasets in your current environment:

```bash
dtx datasets list
```

---

## Selecting a Dataset When Generating a Red Teaming Plan

You can specify a dataset when generating a red teaming plan file. This allows you to control which prompt generator (dataset) is used during test planning.

### Command Syntax

```bash
dtx redteam plan <scope_file.yml> <output_plan_file.yml> --dataset <dataset_name>
```

### Example

```bash
dtx redteam plan sample_langhub_scope.yml sample_langhub_plan.yml --dataset stringray
```

This will generate a `sample_langhub_plan.yml` file based on your scope, using the `STRINGRAY` dataset for prompt generation.

---

## Use Cases

- **Focused Red Teaming**: Choose datasets based on the specific risk category you want to test (e.g., `HF_FLIPGUARDDATA` for text obfuscation attacks).
- **Custom Planning**: Incorporate dataset selection directly into your CI pipelines or scripted test workflows.
- **Multi-pass Testing**: Generate multiple plans using different datasets to test the same model against varied threat types.

