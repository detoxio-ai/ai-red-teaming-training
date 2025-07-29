### 📦 What is `tmux`?

`tmux` is a **terminal multiplexer** — it lets you run multiple shell sessions in one terminal window. You can split windows, run processes in the background, and reconnect later. Perfect for developers, sysadmins, and hackers.

---

### 🚀 Getting Started

#### ✅ 1. Install `tmux`

```bash
sudo apt install tmux       # Ubuntu/Debian
brew install tmux           # macOS
```

---

### 🖥️ 2. Start a Session

```bash
tmux new -s mysession
```

> This opens a new tmux session named `mysession`.

---

### 🧱 3. Split the Terminal into Panes

* **Vertical (side-by-side):**
  `Ctrl+b` then `%`

* **Horizontal (top/bottom):**
  `Ctrl+b` then `"`

---

### 🧭 4. Navigate Between Panes

#### 🔼 Arrow Keys

* `Ctrl+b` then ← → ↑ ↓ to move

#### 🔄 **Shift + Arrow Support**

We'll enable this below using custom key bindings.

---

### 🖱️ 5. Enable Mouse Support (Scroll, Click to Select)

You'll be able to:

* Click to switch between panes
* Scroll using the mouse wheel

---

### ⚙️ 6. Setup Your `~/.tmux.conf`

Create or edit your tmux config file:

```bash
nano ~/.tmux.conf
```

Paste this config:

```tmux
# --- Vim-style navigation ---
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# --- Shift + Arrow keys ---
bind -n S-Left select-pane -L
bind -n S-Right select-pane -R
bind -n S-Up select-pane -U
bind -n S-Down select-pane -D

# --- Mouse support ---
set -g mouse on

# --- Better visuals (optional) ---
set -g status-bg colour235
set -g status-fg white
set -g pane-border-style fg=white
set -g pane-active-border-style fg=brightgreen

# Increase scrollback history size
set -g history-limit 100000

```

Then reload your config:

```bash
tmux source-file ~/.tmux.conf
```

---

### ⏱️ 7. Detach and Resume

* **Detach from session (keep it running):**
  `Ctrl+b` then `d`

* **List all sessions:**

  ```bash
  tmux ls
  ```

* **Reattach to a session:**

  ```bash
  tmux attach -t mysession
  ```

---

### ❌ 8. Exit a tmux Session

* Run `exit` in each pane to close it.
* When all panes are closed, the session ends.

---

### 🧠 Tips & Tricks

* Use `tmux rename-window` to label windows
* Press `Ctrl+b` then `z` to **zoom a pane**
* Run long scripts in one pane while working in another

---

### 🎯 Summary Cheat Sheet

| Action                        | Keys                    |
| ----------------------------- | ----------------------- |
| New session                   | `tmux new -s mysession` |
| Split vertical (side)         | `Ctrl+b` then `%`       |
| Split horizontal (top/bottom) | `Ctrl+b` then `"`       |
| Move (arrows)                 | `Ctrl+b` then ← ↑ ↓ →   |
| Move (vim-style)              | `Ctrl+b` then `h j k l` |
| Move (Shift + arrows)         | `Shift + ← ↑ ↓ →`       |
| Detach                        | `Ctrl+b` then `d`       |
| Reattach                      | `tmux attach -t name`   |
| Enable mouse                  | `set -g mouse on`       |

