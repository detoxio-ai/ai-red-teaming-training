# 🧪 toy_nn – FashionMNIST Classifier with Adversarial Attacks

This project is a minimal neural network training and adversarial attack framework for **FashionMNIST**.  
It supports two modes:

- **train** → Train a simple feed-forward neural network on FashionMNIST and save a checkpoint.
- **attack** → Load a trained checkpoint, perform **FGSM** and **PGD** adversarial attacks, and visualize misclassified examples.

---

## 🚀 Setup

We use [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Create a virtual environment
uv venv .venv
source .venv/bin/activate

# Install dependencies
uv add torch torchvision matplotlib numpy
```

---

## 📂 Project Structure

```
.
├── data/                 # Downloaded FashionMNIST dataset
├── runs/                 # Saved checkpoints & adversarial images
├── main.py               # Entry point (train / attack modes)
├── README.md             # This file
├── pyproject.toml        # uv project config
└── uv.lock               # dependency lockfile
```


## 🧠 How the attacks work

### Threat model (L∞, pixel space)

We add a small perturbation $\delta$ to an input image $x \in [0,1]^{1\times 28\times 28}$ so that the model’s prediction changes, while keeping $\|\delta\|_\infty \le \varepsilon$ (max per-pixel change ≤ ε).
We always **clamp** to the valid image range and **project** back to the ε-ball so the perturbation budget isn’t exceeded.

* **Clamp:** `x = torch.clamp(x, 0.0, 1.0)`
* **Project (L∞):** `x_adv = torch.max(torch.min(x_adv, x + eps), x - eps)`

This repo keeps data in **\[0,1]** (no normalization), so **ε and α are in pixel units** (e.g., `8/255 ≈ 0.031`).

---

### FGSM (Fast Gradient Sign Method, one-step)

Untargeted FGSM takes **one step** in the direction that *increases* loss:

$$
x_{\text{adv}} = \text{clip}_{[0,1]}\Big(x + \varepsilon \cdot \text{sign}\big(\nabla_x \mathcal{L}(f(x), y)\big)\Big)
$$

* In code: `fgsm_attack(...)`
* Steps:

  1. `x.requires_grad_(True)`, forward pass
  2. `loss = NLLLoss(log_probs, y)`; `loss.backward()` to get `x.grad`
  3. Add `eps * sign(x.grad)`, then clamp to `[0,1]`

**Targeted FGSM** (not enabled by default) flips the sign to *decrease* loss toward a chosen target class $t$:
`x_adv = x - eps * sign(∇_x L(f(x), t))`

---

### PGD (Projected Gradient Descent, multi-step)

PGD is an **iterative** version of FGSM with a per-step size $\alpha$ and projection back into the ε-ball each iteration. We also start from a **random point** inside the ε-ball (“random start”) to avoid weak local optima.

Repeat for `steps`:

$$
x^{k+1} = \Pi_{B_\infty(x,\varepsilon)}\Big( \text{clip}_{[0,1]}(x^k + \alpha \cdot \text{sign}(\nabla_x \mathcal{L}(f(x^k), y))) \Big)
$$

* In code: `pgd_attack(...)`
* Key lines:

  * **Random start:** `delta ~ U(-eps, eps)`, `x_adv = clamp(x + delta)`
  * **Update:** `x_adv += alpha * sign(grad)`
  * **Project:** `x_adv = max(min(x_adv, x + eps), x - eps)`
  * **Clamp to image range:** `clamp(0,1)`

---

### Choosing ε (budget) and α (step)

* Common ε (L∞): **`4/255`, `8/255`, `16/255`, `32/255`**
* Rule of thumb for PGD: **α ≈ ε/4 … ε/2**, **steps = 10–40**
* In CLI:

  * `--eps 8,16,32` (interpreted as `/255`), or decimals `--eps 0.031,0.063`
  * `--pgd-alpha auto` picks `max(eps/4, 1/255)`


## 🎓 Training

Train a model for 5 epochs with batch size 64 and save to `./runs/fashion_mnist.pth`:

```bash
python main.py --mode train \
    --epochs 5 \
    --batch-size 64 \
    --ckpt ./runs/fashion_mnist.pth
```

Example output:

```
Epoch 5
-------------------------------
loss: 0.272584 [51200/60000]
Test accuracy: 0.872
Training done!
Saved model to: ./runs/fashion_mnist.pth
```

---

## ⚔️ Adversarial Attack

Run FGSM + PGD attacks against the trained model:

```bash
python main.py --mode attack \
    --ckpt ./runs/fashion_mnist.pth \
    --eps 0.1255 \
    --pgd-steps 20 \
    --pgd-alpha 0.0314 \
    --visualize \
    --no-show \
    --save-dir ./runs
```

This will:

* Print clean accuracy and adversarial accuracy
* Save misclassified adversarial examples:

  * `adv_triptych.png` (clean vs adv vs perturbation)
  * `misclassified_adv_epsXX.png` (single adversarial example)

---

## 📊 Example Results

```
[ATTACK] Loaded ckpt: ./runs/fashion_mnist.pth (meta={'clean_acc': 0.8715, 'epochs': 5}). Clean acc: 0.872

[FGSM] accuracy:
  eps=0.1255: 0.018

[PGD] accuracy:
  eps=0.1255, alpha=0.0314, steps=20: 0.004

Saved triptych to: ./runs/adv_triptych.png
Saved adversarial image to: ./runs/misclassified_adv_eps32.png
```

---

## 🖼️ Visualization

* **Clean** vs **Adversarial** vs **Perturbation** images are saved in `./runs/`
* Perturbation is scaled for visibility

---

## ⚠️ Disclaimer

This is a **toy project** for research & educational purposes only.
Do not use adversarial attack code for malicious purposes.

