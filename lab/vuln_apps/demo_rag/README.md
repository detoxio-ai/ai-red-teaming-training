# Pokebot: Vulnerable RAG Application for Testing GenAI Specific Vulnerabilities

Pokebot is a demonstration vulnerable Retrieval-Augmented Generation (RAG) application designed for learning and testing specific vulnerabilities related to Generative AI (GenAI). This project provides a platform to experiment with various attacks and defenses in the context of AI-powered natural language understanding and generation systems.


## Quick Start

**Navigate to the `demo_rag` Folder and install dependecies**

Before installing dependencies, move to the `demo_rag` folder:

```sh
cd demo_rag
poetry install
poetry shell
```

**Setup OpenAI API Key**

```sh
cp .env.template .env
```
Set your OpenAI API Key to access the model.


**Running the Application**

Start the Pokebot application by providing seed data (optional):
```bash
poetry run pokebot rag start
poetry run pokebot rag start --seed data/med/articles/diabetes.txt
poetry run pokebot rag start --seed data/med/articles/healthcare.txt
```

**Alternatively use Pip**

```bash
pip install -r requirements.txt
python pokebot/main.py --seed data/med/articles/diabetes.txt
```

Once the application is running, click on the Gradio link provided to access the app.

## Usage

### Prompting Without Poisoning Data

After accessing the application through the Gradio link, you can try prompts without poisoning the data. For example:
```text
What is the best medicine for diabetes?
```

### Poisoning Data

To simulate data poisoning, select the "Poison" option and submit. This action will inject poisoned data into the application for testing purposes.

### Trying New Prompts

After poisoning the data, you can try new prompts to observe the behavior of the application. For example:
```text
Get list of usernames
```

## Contributing

Contributions to Pokebot are welcome! If you discover any vulnerabilities, have ideas for improvements, or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

