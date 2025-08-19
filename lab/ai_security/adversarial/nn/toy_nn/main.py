# main.py
import os
import argparse
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib
import matplotlib.pyplot as plt
from torchvision.utils import save_image

# ----------------------------
# Utils: seed / device
# ----------------------------
def set_seed(seed=42, deterministic=True):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

def get_device(use_cuda: bool):
    return torch.device("cuda") if (use_cuda and torch.cuda.is_available()) else torch.device("cpu")

# ----------------------------
# Data
# ----------------------------
def build_loaders(data_root="./data", batch_size=64, workers=2):
    tf = transforms.Compose([transforms.ToTensor()])
    train_ds = datasets.FashionMNIST(root=data_root, train=True, download=True, transform=tf)
    test_ds  = datasets.FashionMNIST(root=data_root, train=False, download=True, transform=tf)
    train_ld = DataLoader(train_ds, batch_size=batch_size, shuffle=True,  num_workers=workers)
    test_ld  = DataLoader(test_ds,  batch_size=batch_size, shuffle=False, num_workers=workers)
    return train_ld, test_ld

CLASS_NAMES = [
    "T-shirt/top","Trouser","Pullover","Dress","Coat",
    "Sandal","Shirt","Sneaker","Bag","Ankle boot"
]

# ----------------------------
# Model
# ----------------------------
class FashionMNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
            nn.LogSoftmax(dim=1)   # pairs with NLLLoss
        )
    def forward(self, x):
        x = self.flatten(x)
        return self.linear_relu_stack(x)

# ----------------------------
# Train/Eval helpers
# ----------------------------
def train_one_epoch(dataloader, model, loss_fn, optimizer, device):
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        pred = model(X)
        loss = loss_fn(pred, y)
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        if batch % 100 == 0:
            current = batch * len(X)
            total = len(dataloader.dataset)
            print(f"loss: {loss.item():>7f} [{current:>5d}/{total:>5d}]")

@torch.no_grad()
def test_accuracy(model, dataloader, device):
    model.eval()
    correct = total = 0
    for X, y in dataloader:
        X, y = X.to(device), y.to(device)
        pred = model(X).argmax(1)
        correct += (pred == y).sum().item()
        total += y.numel()
    return correct / max(total, 1)

def fit(model, train_loader, test_loader, loss_fn, optimizer, device, epochs=5):
    for ep in range(1, epochs + 1):
        print(f"Epoch {ep}\n-------------------------------")
        train_one_epoch(train_loader, model, loss_fn, optimizer, device)
        acc = test_accuracy(model, test_loader, device)
        print(f"Test accuracy: {acc:.3f}")
    print("Training done!")

# ----------------------------
# Save / Load
# ----------------------------
def save_model(model, path, meta=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    payload = {"state_dict": model.state_dict(), "arch": "FashionMNISTModel", "meta": meta or {}}
    torch.save(payload, path)
    print(f"Saved model to: {path}")

def load_model(path, device):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    ckpt = torch.load(path, map_location=device)
    model = FashionMNISTModel().to(device)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()
    print(f"Loaded model from: {path}")
    return model, ckpt.get("meta", {})

# ----------------------------
# Attacks (L∞)
# ----------------------------
def fgsm_attack(model, x, y, eps, loss_fn):
    was_training = model.training
    model.eval()
    x = x.clone().detach().requires_grad_(True)
    y = y.clone().detach()
    out = model(x); loss = loss_fn(out, y)
    model.zero_grad(); loss.backward()
    x_adv = x + eps * x.grad.sign()
    x_adv = torch.clamp(x_adv, 0.0, 1.0).detach()
    if was_training: model.train()
    return x_adv

def pgd_attack(model, x, y, eps=8/255, alpha=2/255, steps=10, loss_fn=None):
    if loss_fn is None: loss_fn = nn.NLLLoss()
    was_training = model.training
    model.eval()
    x = x.clone().detach()
    y = y.clone().detach()
    delta = torch.empty_like(x).uniform_(-eps, eps)
    x_adv = torch.clamp(x + delta, 0.0, 1.0).detach()
    for _ in range(steps):
        x_adv.requires_grad_(True)
        out = model(x_adv); loss = loss_fn(out, y)
        model.zero_grad(); loss.backward()
        with torch.no_grad():
            x_adv = x_adv + alpha * x_adv.grad.sign()
            x_adv = torch.max(torch.min(x_adv, x + eps), x - eps)  # project to L∞ ball
            x_adv = torch.clamp(x_adv, 0.0, 1.0).detach()
    if was_training: model.train()
    return x_adv

def adv_accuracy(model, dataloader, device, attack_fn, **attack_kwargs):
    model.eval()
    correct = total = 0
    for X, y in dataloader:
        X, y = X.to(device), y.to(device)
        with torch.enable_grad():
            X_adv = attack_fn(model, X, y, **attack_kwargs)
        with torch.no_grad():
            pred = model(X_adv).argmax(1)
        correct += (pred == y).sum().item()
        total += y.numel()
    return correct / max(total, 1)

# ----------------------------
# Noise generators
# ----------------------------
def add_gaussian_noise(x, std=0.05):
    if std <= 0: return x
    return torch.clamp(x + torch.randn_like(x) * std, 0.0, 1.0)

def add_salt_pepper_noise(x, p=0.02):
    # p is per-pixel flip prob; we split equally for salt (1) and pepper (0)
    if p <= 0: return x
    noise = torch.rand_like(x)
    x_sp = x.clone()
    x_sp[noise < (p / 2)] = 0.0
    x_sp[noise > 1 - (p / 2)] = 1.0
    return x_sp

# ----------------------------
# HARDEN: adversarial + noisy re-training
# ----------------------------
def parse_eps_list(arg: str):
    """CSV like '8,16,32' (as /255) or floats '0.031,0.063'."""
    eps_list = []
    for tok in arg.split(","):
        tok = tok.strip()
        if not tok: continue
        val = float(tok)
        eps_list.append(val/255.0 if val > 1.0 else val)
    return eps_list

def parse_alpha(arg: str, eps: float):
    """'auto' => max(eps/4, 1/255). Otherwise numeric; >1 treated as /255."""
    if isinstance(arg, str) and arg.lower() == "auto":
        return max(eps/4.0, 1/255.0)
    val = float(arg)
    return val/255.0 if val > 1.0 else val

def harden_one_epoch(
    train_loader, model, loss_fn, optimizer, device,
    adv_frac=0.5, noise_frac=0.3,
    eps_choices=(8/255,), alpha="auto", steps=5,
    gauss_std=0.05, sp_prob=0.02
):
    """
    Mix each batch with:
      - adv_frac portion: PGD adversarial examples
      - noise_frac portion: noisy inputs (Gaussian + salt&pepper)
      - (1 - adv_frac - noise_frac) portion: clean
    """
    assert 0.0 <= adv_frac <= 1.0 and 0.0 <= noise_frac <= 1.0 and adv_frac + noise_frac <= 1.0, \
        "adv_frac + noise_frac must be <= 1.0"
    model.train()
    for batch, (X, y) in enumerate(train_loader):
        X, y = X.to(device), y.to(device)
        n = X.size(0)
        idx_perm = torch.randperm(n, device=device)

        n_adv   = int(n * adv_frac)
        n_noise = int(n * noise_frac)
        n_clean = n - n_adv - n_noise

        idx_adv   = idx_perm[:n_adv]
        idx_noise = idx_perm[n_adv:n_adv+n_noise]
        idx_clean = idx_perm[n_adv+n_noise:]

        X_mix = torch.empty_like(X)
        y_mix = y.clone()

        # --- Adversarial subset (PGD) ---
        if n_adv > 0:
            eps = random.choice(list(eps_choices))
            alpha_val = parse_alpha(alpha, eps)
            with torch.enable_grad():
                X_adv = pgd_attack(model, X[idx_adv], y[idx_adv],
                                   eps=eps, alpha=alpha_val, steps=steps, loss_fn=loss_fn)
            X_mix[idx_adv] = X_adv

        # --- Noisy subset ---
        if n_noise > 0:
            Xn = add_gaussian_noise(X[idx_noise], std=gauss_std)
            # Apply S&P to half of them for variety
            if n_noise > 1:
                half = n_noise // 2
                Xn_sp = add_salt_pepper_noise(Xn[:half], p=sp_prob)
                Xn = torch.cat([Xn_sp, Xn[half:]], dim=0)
            X_mix[idx_noise] = Xn

        # --- Clean subset ---
        if n_clean > 0:
            X_mix[idx_clean] = X[idx_clean]

        # --- Train step on the mixed batch ---
        pred = model(X_mix)
        loss = loss_fn(pred, y_mix)
        optimizer.zero_grad(); loss.backward(); optimizer.step()

        if batch % 100 == 0:
            current = batch * len(X)
            total = len(train_loader.dataset)
            print(f"[harden] loss: {loss.item():>7f} [{current:>5d}/{total:>5d}]")

def run_harden(
    args,
    *,
    quick_eval_eps=(8/255,)
):
    """
    Fine-tune the saved model with adversarial + noisy examples, then save hardened checkpoint.
    """
    set_seed(args.seed, deterministic=args.deterministic)
    device = get_device(use_cuda=not args.no_cuda)
    print("Device:", device)

    train_loader, test_loader = build_loaders(args.data_root, args.batch_size, args.workers)

    # Load base model
    model, meta = load_model(args.ckpt, device)
    loss_fn = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.harden_lr)

    eps_choices = tuple(parse_eps_list(args.harden_eps))

    print(f"[HARDEN] Starting robust fine-tuning for {args.harden_epochs} epoch(s)")
    print(f"         adv_frac={args.adv_frac}, noise_frac={args.noise_frac}, eps_choices={eps_choices}, steps={args.harden_steps}")

    for ep in range(1, args.harden_epochs + 1):
        print(f"--- Harden Epoch {ep}/{args.harden_epochs} ---")
        harden_one_epoch(
            train_loader, model, loss_fn, optimizer, device,
            adv_frac=args.adv_frac, noise_frac=args.noise_frac,
            eps_choices=eps_choices, alpha=args.harden_alpha, steps=args.harden_steps,
            gauss_std=args.noise_gauss_std, sp_prob=args.noise_sp_prob
        )
        acc = test_accuracy(model, test_loader, device)
        print(f"[HARDEN] epoch {ep} clean test acc: {acc:.3f}")

        # quick adversarial spot-check
        for eps in quick_eval_eps:
            spot = adv_accuracy(model, test_loader, device, pgd_attack,
                                eps=eps, alpha=parse_alpha("auto", eps), steps=5, loss_fn=loss_fn)
            print(f"[HARDEN] epoch {ep} quick PGD acc (eps={eps:.4f}, 5 steps): {spot:.3f}")

    # Save hardened model
    meta_out = dict(meta or {})
    meta_out.update({
        "hardened": True,
        "harden_epochs": args.harden_epochs,
        "adv_frac": args.adv_frac,
        "noise_frac": args.noise_frac,
        "eps_choices": eps_choices,
        "harden_steps": args.harden_steps,
        "noise_gauss_std": args.noise_gauss_std,
        "noise_sp_prob": args.noise_sp_prob
    })
    save_model(model, args.ckpt_out, meta=meta_out)
    print(f"[HARDEN] Saved hardened checkpoint to {args.ckpt_out}")

# ----------------------------
# Visualization (headless-safe)
# ----------------------------
def show_and_save_first_misclassified_adv(
    model, dataloader, device, loss_fn,
    eps_list, steps=20, save_dir=".", show=True
):
    os.makedirs(save_dir, exist_ok=True)
    for eps in eps_list:
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            with torch.enable_grad():
                alpha = max(eps / 4, 1/255)
                X_adv = pgd_attack(model, X, y, eps=eps, alpha=alpha, steps=steps, loss_fn=loss_fn)
            with torch.no_grad():
                pred_clean = model(X).argmax(1)
                pred_adv   = model(X_adv).argmax(1)
            mismatch = (pred_adv != y)
            if mismatch.any():
                idx = mismatch.nonzero(as_tuple=True)[0][0].item()
                x_cl = X[idx].detach().cpu()
                x_ad = X_adv[idx].detach().cpu()
                y_t  = y[idx].item()
                pc   = pred_clean[idx].item()
                pa   = pred_adv[idx].item()

                fig, axes = plt.subplots(1, 3, figsize=(9, 3))
                axes[0].imshow(x_cl.squeeze().numpy(), cmap="gray")
                axes[0].set_title(f"Clean\ntrue: {CLASS_NAMES[y_t]}\npred: {CLASS_NAMES[pc]}")
                axes[0].axis("off")
                axes[1].imshow(x_ad.squeeze().numpy(), cmap="gray")
                axes[1].set_title(f"Adversarial (ε={eps:.4f})\npred: {CLASS_NAMES[pa]}")
                axes[1].axis("off")
                delta = (x_ad - x_cl).squeeze().numpy()
                d = delta / (np.max(np.abs(delta)) + 1e-8)
                axes[2].imshow(d, cmap="gray")
                axes[2].set_title("Perturbation (scaled)")
                axes[2].axis("off")
                plt.tight_layout()

                triptych_path = os.path.join(save_dir, "adv_triptych.png")
                backend = matplotlib.get_backend().lower()
                interactive = any(k in backend for k in ["qt", "tk", "macosx", "inline"])
                if show and interactive:
                    plt.show()
                plt.savefig(triptych_path, bbox_inches="tight")
                plt.close(fig)

                adv_path = os.path.join(save_dir, f"misclassified_adv_eps{int(round(eps*255))}.png")
                save_image(x_ad, adv_path)
                print(f"Saved triptych to: {triptych_path}")
                print(f"Saved adversarial image to: {adv_path}")
                return adv_path
    print("No misclassified adversarial example found. Try larger eps or more steps.")
    return None

# ----------------------------
# Modes: train / attack / harden
# ----------------------------
def run_train(args):
    set_seed(args.seed, deterministic=args.deterministic)
    device = get_device(use_cuda=not args.no_cuda)
    print("Device:", device)

    train_loader, test_loader = build_loaders(args.data_root, args.batch_size, args.workers)
    model = FashionMNISTModel().to(device)
    loss_fn = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    fit(model, train_loader, test_loader, loss_fn, optimizer, device, epochs=args.epochs)
    clean_acc = test_accuracy(model, test_loader, device)
    save_model(model, args.ckpt, meta={"clean_acc": clean_acc, "epochs": args.epochs})
    print(f"[TRAIN] Saved checkpoint to {args.ckpt}. Clean test acc: {clean_acc:.3f}")

def run_attack(args):
    set_seed(args.seed, deterministic=args.deterministic)
    device = get_device(use_cuda=not args.no_cuda)
    print("Device:", device)

    _, test_loader = build_loaders(args.data_root, args.batch_size, args.workers)
    model, meta = load_model(args.ckpt, device)
    loss_fn = nn.NLLLoss()

    eps_list = parse_eps_list(args.eps)
    clean_acc = test_accuracy(model, test_loader, device)
    print(f"[ATTACK] Loaded ckpt: {args.ckpt} (meta={meta}). Clean acc: {clean_acc:.3f}")

    if args.eval_attack in ("fgsm","both"):
        print("\n[FGSM] accuracy:")
        for eps in eps_list:
            acc = adv_accuracy(model, test_loader, device, fgsm_attack, eps=eps, loss_fn=loss_fn)
            print(f"  eps={eps:.4f}: {acc:.3f}")

    if args.eval_attack in ("pgd","both"):
        print("\n[PGD] accuracy:")
        for eps in eps_list:
            alpha = parse_alpha(args.pgd_alpha, eps)
            acc = adv_accuracy(model, test_loader, device, pgd_attack,
                               eps=eps, alpha=alpha, steps=args.pgd_steps, loss_fn=loss_fn)
            print(f"  eps={eps:.4f}, alpha={alpha:.4f}, steps={args.pgd_steps}: {acc:.3f}")

    if args.visualize:
        if args.no_show:
            matplotlib.use("Agg")
        show_and_save_first_misclassified_adv(
            model, test_loader, device, loss_fn,
            eps_list=eps_list,
            steps=max(20, args.pgd_steps),
            save_dir=args.save_dir,
            show=not args.no_show
        )

# ----------------------------
# Main (CLI)
# ----------------------------
def main():
    ap = argparse.ArgumentParser(description="FashionMNIST modes: train | attack | harden")
    ap.add_argument("--mode", choices=["train","attack","harden"], default="train", help="Run mode")

    # shared I/O & env
    ap.add_argument("--ckpt", type=str, default="./runs/fashion_mnist.pth", help="(train/attack) checkpoint path")
    ap.add_argument("--data-root", type=str, default="./data")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--deterministic", action="store_true")
    ap.add_argument("--no-cuda", action="store_true")

    # train args
    ap.add_argument("--epochs", type=int, default=5)
    ap.add_argument("--lr", type=float, default=1e-3)

    # attack args
    ap.add_argument("--eval-attack", choices=["fgsm","pgd","both"], default="both")
    ap.add_argument("--eps", type=str, default="8,16,32", help="CSV eps; ints as /255 or floats in [0,1]")
    ap.add_argument("--pgd-steps", type=int, default=20)
    ap.add_argument("--pgd-alpha", type=str, default="auto")
    ap.add_argument("--visualize", action="store_true")
    ap.add_argument("--save-dir", type=str, default="./runs")
    ap.add_argument("--no-show", action="store_true")

    # harden args
    ap.add_argument("--ckpt-out", type=str, default="./runs/fashion_mnist_hardened.pth", help="Output hardened checkpoint")
    ap.add_argument("--harden-epochs", type=int, default=3, help="Fine-tuning epochs")
    ap.add_argument("--harden-lr", type=float, default=5e-4, help="LR during hardening")
    ap.add_argument("--adv-frac", type=float, default=0.5, help="Fraction of batch made adversarial")
    ap.add_argument("--noise-frac", type=float, default=0.3, help="Fraction of batch made noisy (rest is clean)")
    ap.add_argument("--harden-eps", type=str, default="8,16", help="CSV eps for PGD during hardening")
    ap.add_argument("--harden-steps", type=int, default=5, help="PGD steps during hardening")
    ap.add_argument("--harden-alpha", type=str, default="auto", help="'auto' or numeric (per-255 if >1)")
    ap.add_argument("--noise-gauss-std", type=float, default=0.05, help="Gaussian noise std")
    ap.add_argument("--noise-sp-prob", type=float, default=0.02, help="Salt & pepper prob per pixel")

    args = ap.parse_args()

    if args.mode == "train":
        run_train(args)
    elif args.mode == "attack":
        run_attack(args)
    else:
        run_harden(args)

if __name__ == "__main__":
    main()
