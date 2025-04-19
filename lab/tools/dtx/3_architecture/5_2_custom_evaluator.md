
# Overview: Custom Evaluator

## How to Evaluate Custom Responses from the Target

When testing a target model or endpoint that returns structured JSON (e.g., with fields like `toxicity`, `JAILBREAK`, `classification`), you need to define **how those outputs are evaluated** to determine if a response is risky or flagged.

This is done using a `global_evaluator`.

### There Are Two Ways to Provide an Evaluator

#### 1. Use `--eval` flag during redteam execution

```bash
dtx redteam run plan.yml --eval ibm
```

This applies a predefined evaluator (like `ibm`, `openai`, or `jsonpath`) at runtime.

#### 2. Define a `global_evaluator` inside your plan or scope YAML file

This gives you full control with custom rules, response parsing, and JSONPath-based expressions.

---

## YAML Example: Evaluating a Custom API Response

Let’s say your provider returns the following JSON:

```json
{
  "response": {
    "JAILBREAK": 0.93,
    "INJECTION": 0.45
  }
}
```

You want to flag a response if any risk score exceeds `0.8`.

### Sample Plan or Scope YAML

```yaml
redteam:
  global_evaluator:
    evaluation_method:
      eval_model_type: "JSON_EXPRESSION"
      eval_model_name: "ANY_JSONPATH_EXP"
      scope: "response"
      expressions:
        - "any(.response | to_entries[]; .value > 0.8)"
```

### How It Works

- `scope: response` tells the evaluator to look inside the `response` field.
- The expression `any(.response | to_entries[]; .value > 0.8)` flags the output if **any** key (e.g., `JAILBREAK`, `INJECTION`) has a score over `0.8`.

---

## YAML Example: Matching Specific Score Label (e.g., Hugging Face)

Response:

```json
{
  "scores": {
    "LABEL_0": 0.12,
    "LABEL_1": 0.91
  }
}
```

YAML:

```yaml
redteam:
  global_evaluator:
    evaluation_method:
      eval_model_type: "JSON_EXPRESSION"
      eval_model_name: "ANY_JSONPATH_EXP"
      scope: "scores"
      expressions:
        - ".scores.LABEL_1 | select(. > 0.8)"
```

This flags results where `LABEL_1` (often used for "toxic" or "unsafe") is above `0.8`.

---

## YAML Example: LLaMA Guard Response from Ollama

Response:

```json
{
  "response": {
    "content": "unsafe"
  }
}
```

YAML:

```yaml
redteam:
  global_evaluator:
    evaluation_method:
      eval_model_type: "JSON_EXPRESSION"
      eval_model_name: "ANY_JSONPATH_EXP"
      scope: "response"
      expressions:
        - '.response.content | contains("unsafe")'
```

This flags any response where the content explicitly says `"unsafe"`.

---

## YAML Example: Multiple Rule Checks

Response:

```json
{
  "result": {
    "classification": "violation",
    "score": 0.94
  }
}
```

YAML:

```yaml
redteam:
  global_evaluator:
    evaluation_method:
      eval_model_type: "JSON_EXPRESSION"
      eval_model_name: "ANY_JSONPATH_EXP"
      scope: "result"
      expressions:
        - '.classification | contains("violation")'
        - '.score | select(. > 0.9)'
```

This checks both conditions: the classification must be `"violation"` **and** the score must be above `0.9`.

---

## Example With `transform_response`

If your API returns a large nested structure, you can pre-process it using `transform_response`.

```yaml
providers:
  - id: "http"
    config:
      raw_request: |
        POST /evaluate HTTP/1.1
        Host: {{ENV_HOST}}
        Authorization: Bearer {{TOKEN}}
        Content-Type: application/json

        {
          "texts": ["{{prompt}}"]
        }
      transform_response: |
        {
          "response": {
            "JAILBREAK": json["results"][0]["chunk_results"][0]["JAILBREAK"],
            "INJECTION": json["results"][0]["chunk_results"][0]["INJECTION"]
          }
        }
```

Then apply the same `global_evaluator` logic to the extracted structure.

---
