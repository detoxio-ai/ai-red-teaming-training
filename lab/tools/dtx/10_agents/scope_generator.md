# Agents Scope Generator

## Overview
The **Agents Scope Generator** is a security assessment script that utilizes AI models to generate a red team scope based on the provided target. It processes information interactively and can produce structured output in YAML format.

## Installation & Setup
Ensure you have Python installed and any required dependencies.

To install the extension with additional features, use:

```sh
poetry install --extras autogen
```

## Usage
Run the script with the required parameters:

```sh
poetry run python dtx/plugins/agents/autogen/agents_scope_generator.py --target <TARGET_URL>
```

### Command-line Arguments
| Argument               | Description                                      | Required | Default |
|------------------------|--------------------------------------------------|----------|---------|
| `--target <URL>`      | Specifies the target URL or name.              | ✅       | N/A     |
| `-v, --verbose`       | Enables verbose output for detailed logs.       | ❌       | False   |
| `-i, --interactive`   | Enables interactive mode.                        | ❌       | False   |
| `-o, --output <file>` | Specifies the output file name (YAML format).   | ❌       | `morphius_scope.yml` |
| `-m, --model <name>`  | Specifies the AI model to use.                   | ❌       | `gpt-4o` |

### Example Usage
**Basic execution:**
```sh
poetry run python dtx/plugins/agents/autogen/agents_scope_generator.py --target https://x.com/nft_xbt
```

**Custom output file and verbose mode:**
```sh
poetry run python dtx/plugins/agents/autogen/agents_scope_generator.py --target https://x.com/nft_xbt -o morphius_xbt_scope.yml -v
```

**Interactive mode:**
```sh
poetry run python dtx/plugins/agents/autogen/agents_scope_generator.py --target https://x.com/nft_xbt -i
```

## Output
The script generates a structured YAML file containing the red team scope details, which can be used for further analysis.

## Notes
- Ensure you have API access to the AI model specified (`gpt-4o` by default).
- The `interactive` mode may require user input during execution.
