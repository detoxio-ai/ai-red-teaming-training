# Quick Start Guide
Text2SQL Toolkit is a demo project that converts natural language queries into SQL commands and executes them against a SQLite database. It leverages OpenAI's language model, LangChain Community modules, and Gradio to provide an interactive and visually appealing query interface.

## Setup Instructions

### 1. Navigate to the `demo` Folder

Before installing dependencies, move to the `demo_text2sql_toolkit` folder:

```sh
cd demo_text2sql_toolkit
```

### 2. Copy `.env.template` to `.env` and Update `OPENAI_API_KEY`

```sh
cp .env.template .env
```

Open the newly created `.env` file and set your OpenAI API Key to access the model.

### 3. Install Dependencies Using Poetry

```sh
poetry install
```

If you don’t have Poetry installed, use:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 4. Activate Poetry Shell (to activate the environment)

```sh
poetry shell
```

If needed, install the Poetry Shell plugin:

```sh
poetry self add poetry-plugin-shell
```

### 5. Run the Application Using Gradio

```sh
python main.py
```

You can access the SQL natural language query UI at: `http://localhost:7860`

---

## How It Works 🛡️

1. **User Input:** The application receives a natural language query describing the SQL operation you wish to perform.
2. **SQL Agent:** Using the OpenAI API and the LangChain Community modules, the agent translates your natural language input into an executable SQL query.
3. **Database Execution:** The SQL query is executed against a SQLite database (located in the `db` folder).
4. **Result Presentation:** The results are returned and rendered as a styled HTML table (or preformatted text) in a Gradio interface for easy viewing.

---

## API Reference 📝

### Endpoint

The application runs locally at:

```
http://localhost:7860
```

### Inputs

| Parameter   | Type     | Description                                            |
| ----------- | -------- | ------------------------------------------------------ |
| `SQL Query` | `string` | A natural language description of the desired SQL query. |

### Outputs

| Response       | Description                                                     |
| -------------- | --------------------------------------------------------------- |
| `Query Result` | The SQL query result, rendered as a styled HTML table or text.  |

---

## Additional Information

- **Project Structure:**  
  - `sql2text.py`: Contains the SQL agent configuration and natural language processing setup.
  - `main.py`: Implements the Gradio interface that accepts queries and displays results.
  - `db/`: Directory containing the SQLite database file.
  - `.env.template`: Template for environment variables (e.g., OpenAI API Key).

---
  