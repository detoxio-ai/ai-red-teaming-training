## 🛠️ Generating a Gradio Provider

The `GradioProviderGenerator` is an interactive CLI tool that helps you create provider configurations from **Gradio-hosted APIs**, such as those on **Hugging Face Spaces** or standalone **Gradio app URLs**.

---


### 🚀 How to Use

Run the CLI and follow the interactive prompts:

```bash
python main.py providers generate gradio --url <your_gradio_url_or_space>
```

Replace `<your_gradio_url_or_space>` with either a Hugging Face Space name or a full Gradio app URL.

---


### 🔗 Supported url Input Options

You can initialize the generator using either:

1. **Hugging Face Space name**  
   Format: `username/space_name`  
   Example: `detoxioai/Pokebot`

2. **Direct Gradio app URL**  
   Example: `https://medusa.detoxio.dev`


---

### 🧭 Walkthrough

1. **Inspect or Generate:** Choose whether you want to inspect available APIs or directly generate a provider.

2. **Select APIs:** The tool lists all available API endpoints. Choose one or more to include.

3. **Configure Parameters:**  
   For each selected API:
   - Enter values for parameters.
   - If a parameter accepts multiple options (e.g., `Literal`), you'll be prompted to pick one.
   - Jinja template syntax like `{{prompt}}` can be used for dynamic inputs.

4. **Response Parsing (Auto-Detected):**  
   The tool will analyze the response and suggest a parsing strategy using:
   - `parser_type`: Signature-based parsing
   - `content_type`: e.g., `array`, `json`
   - `location`: Index path to the desired value in the response

5. **Save Configuration:**  
   After generation, the provider configuration is saved as a `.yaml` file (default: `gradio_providers.yaml`).

---

### ✅ Example Output

```bash
❯ python main.py providers generate gradio --url https://medusa.detoxio.dev

╭───────────────────────────╮
│ Gradio Provider Generator │
╰───────────────────────────╯

Do you want to (1) Inspect APIs or (2) Generate Providers? (Enter 1 or 2) (2): 2

   Available APIs   
┏━━━━━━━┳━━━━━━━━━━┓
┃ Index ┃ API Path ┃
┡━━━━━━━╇━━━━━━━━━━┩
│   1   │ /greet   │
│   2   │ /greet_1 │
│   3   │ /greet_2 │
└───────┴──────────┘

Enter the numbers of the APIs you want to use (comma-separated) (): 1

╭────────────────────────────────────────╮
│ Configuring parameters for API: /greet │
╰────────────────────────────────────────╯

Enter value for 'prompt' (press Enter to keep default: None) (): {{prompt}}
Enter value for 'detoxio_api_key' (press Enter to keep default: ) (): 
Choose a value for 'challenge' from: Your Math Assistant, Your SQL DB Assistant, GPT Leaky Assistant, Your Fintech Assistant, GPT Text2SQL Agent
Enter value for 'challenge' (press Enter to keep default: Your Math Assistant) (Your Math Assistant): 
Choose a value for 'challenge_level' from: easy, easy, medium, medium, medium
Enter value for 'challenge_level' (press Enter to keep default: easy) (easy): 

Provider generated successfully!
Loaded as API: https://medusa.detoxio.dev/ ✔

Generated Response Location : `{'parser_type': 'signature', 'content_type': 'array', 'location': [1, -1, 1]}`

Do you want to exit? (yes/no) (yes): yes
Enter filename to save as (default: gradio_providers.yaml) (gradio_providers.yaml): y
Configuration saved to y ✅
```

---

### 📁 Output File (`y`)

```yaml
providers:
  - id: gradio
    config:
      url: https://medusa.detoxio.dev
      apis:
        - path: /greet
          params:
            - name: prompt
              value: '{{prompt}}'
            - name: detoxio_api_key
              value: ''
            - name: challenge
              value: Your Math Assistant
            - name: challenge_level
              value: easy
          transform_response:
            parser_type: signature
            content_type: array
            location:
              - 1
              - -1
              - 1
```
