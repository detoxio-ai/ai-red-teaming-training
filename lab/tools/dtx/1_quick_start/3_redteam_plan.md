# **🧩 Custom Red Team Workflow (Scope → Plan → Run)**

This guide shows how to **manually control** your red teaming workflow by generating a scope and plan, and then executing the test.

Ideal if you want to:
- ✅ Customize scope
- ✅ Reuse the plan later
- ✅ Test workflows step by step

---

## ✅ Step 1: Generate a Red Teaming Scope

The **scope** defines the target AI agent and the security objectives for testing.

```bash
dtx redteam scope "This is my dummy agent" redteam_scope.yml
```

✅ Result:  
Creates `redteam_scope.yml`, describing your **dummy agent**.

> **Tip:**  
> You can edit `redteam_scope.yml` to customize objectives or testing scope!

---

## ✅ Step 2: Generate a Red Teaming Plan

The **plan** builds structured test cases based on the scope and dataset.  
Here, we'll use **AISafety** dataset — safe to combine with evaluators.

```bash
dtx redteam plan redteam_scope.yml redteam_plan.yml --dataset aisafety
```

✅ Result:  
Creates `redteam_plan.yml` with **attack scenarios** and evaluation criteria based on the **AISafety** dataset.

> 🔍 **Why AISafety?**  
> - ✅ Safe for evaluator pairing
> - ✅ Contains real-world safety and alignment scenarios

---

## ✅ Step 3: Run the Red Teaming Plan

The **run** phase executes the plan using the **ECHO dummy agent**.  
We'll evaluate outputs using the **IBM Granite HAP 38M** evaluator.

```bash
dtx redteam run echo --plan redteam_plan.yml --eval ibm38
```

✅ Result:
- Executes red teaming test cases
- Simulates agent responses (ECHO agent)
- Evaluates outputs with **IBM model**

> **Optional:** Add `--max_prompts 10` to limit number of prompts.

---

## ✅ Summary Table

| Step | Command | Purpose |
|------|---------|----------|
| 1️⃣ Scope | `dtx redteam scope "This is my dummy agent" redteam_scope.yml` | Define red teaming objectives |
| 2️⃣ Plan | `dtx redteam plan redteam_scope.yml redteam_plan.yml --dataset aisafety` | Generate test scenarios |
| 3️⃣ Run  | `dtx redteam run echo --plan redteam_plan.yml --eval ibm38` | Execute the tests |

---

## ✅ Notes & Recommendations

- ⚠️ If using **garak** dataset, skip `--eval`:
  ```bash
  dtx redteam plan redteam_scope.yml redteam_plan.yml --dataset stingray
  dtx redteam run echo --plan redteam_plan.yml
  ```

- ✅ Use `echo` agent for fast local dry runs.
- ✅ For real models, switch `echo` to:
  ```bash
  dtx redteam run hf_model --url arnir0/Tiny-LLM --plan redteam_plan.yml --eval ibm38
  ```

- ✅ Customize your plan! You can manually edit `redteam_plan.yml` for advanced scenarios.

---

## ✅ Next Steps

- ✅ Explore datasets: `dtx datasets list`
- ✅ Explore evaluators: `dtx tactics list`
- ✅ Try different evaluators: `--eval ibm125`, `--eval keyword --keywords research`
