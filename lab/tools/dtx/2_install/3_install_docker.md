# Docker Installation (`ddtx`)

This guide explains how to set up and use **dtx** with Docker via the `ddtx` CLI wrapper.

Using Docker allows you to:
- Avoid local Python and dependency installations
- Run `dtx` fully containerized
- Easily manage environments and avoid conflicts

---

## Prerequisites

- **Docker** installed and running
- **Python** (only for installing `dtx` wrapper locally)

Verify Docker installation:

```bash
docker --version
```

Ensure Docker daemon is running.

---

## Step 1: Install dtx (for access to `ddtx` CLI)

Install the core Python package:

```bash
pip install dtx
```

This installs:
- `dtx` — Local CLI (It will not work without troch installed locally)
- `ddtx` — Docker CLI wrapper

---

## Step 2: Verify ddtx CLI is available

Check:

```bash
ddtx --help
```

You should see the same command structure as `dtx`.

---

## Step 4: Run dtx commands inside Docker

Now you can run any `dtx` command inside Docker using `ddtx`.

Example: Generate a red teaming scope

```bash
ddtx redteam scope "My agent description" scope.yml
```

Example: Generate a red teaming plan

```bash
ddtx redteam plan scope.yml plan.yml --dataset STRINGRAY
```

Example: List available datasets

```bash
ddtx datasets list
```

---

## Notes

- **No need to install torch or other dependencies locally.**
- `ddtx` will mount your working directory and `.env` automatically.
- Files will be stored in your local filesystem under:
  
  ```
  ~/.dtx/
  ```

- For advanced Docker configuration (volumes, env vars), see the Docker CLI documentation.
