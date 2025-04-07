
## 🌐 Generating an HTTP Provider (Browser-Assisted)

The HTTP provider generator enables you to capture real web requests by **interacting directly with a browser**, using Playwright under the hood. This is ideal for non-API-first applications where interaction flows through a frontend.

---

### ✅ Prerequisites

Make sure you’ve installed the project with browser support:

```bash
poetry install --extras playwright
```

Then install Playwright browsers (only once):

```bash
poetry run playwright install
```

---

### 🚀 How It Works

1. The tool launches a real browser session via Playwright.
2. You browse the app (e.g., `https://kissan.ai/chat`) and insert the placeholder `FUZZ` where the dynamic prompt goes.
3. When done, close the browser.
4. The tool captures the request, parses it, and builds a complete provider config.

---

### 🧪 Starting the Capture

```bash
python main.py providers generate http --url https://kissan.ai/chat
```

**You'll be prompted to open the browser:**

```
Do you want to open a browser and start capturing requests for https://kissan.ai/chat? [y/n]: y
```

Once the browser opens:
- Paste `FUZZ` into a relevant field (usually a prompt or input).
- Submit the request.
- Close the browser when you're done.

---

### 📦 Example Console Output

```bash
❯ python main.py providers generate http --url https://kissan.ai/chat

Do you want to open a browser and start capturing requests for https://kissan.ai/chat? [y/n]: y

╭────────────────────── 🧪 Insert FUZZ and Close Browser ───────────────────────╮
│ Please insert your FUZZ marker into the prompt or input field in the browser. │
│ Once done, close the browser to generate provider configuration.              │
╰───────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────── ⚙️ Provider Builder ─────────────────────────────╮
│ Building provider configurations...                                         │
│ This step will analyze requests and convert them to reproducible providers. │
╰─────────────────────────────────────────────────────────────────────────────╯

Converting requests... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

✅ Successfully built 1 providers.
Configuration saved to http_providers.yml ✅
```

---

### 🧾 Sample Output File (`http_providers.yml`)

```yaml
providers:
  - id: http
    config:
      max_retries: 3
      validate_response: status == 200
      transform_request: null
      transform_response: json
      example_response: '{"answer":"...","question":"FUZZ"}'
      raw_request: |
        POST /v1/inference/text/web HTTP/1.1
        Host: {{ENV_HOST}}
        Content-Type: multipart/form-data; boundary=...
        ...
        ------WebKitFormBoundary...
        Content-Disposition: form-data; name="question"

        {{prompt}}
        ...
      use_https: true
environments:
  - vars:
      ENV_HOST: env.ENV_HOST
```

---

### 💡 Tips

- Always use `{{prompt}}` or `FUZZ` to mark where dynamic input should be.
- If there are dynamic hosts or headers, they’ll be extracted into `ENV` variables automatically.
- Works best with `POST` forms, JSON APIs, and multi-part submissions.
