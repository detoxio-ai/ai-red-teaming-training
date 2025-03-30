# Pokebot: Vulnerable RAG Application for Testing GenAI Specific Vulnerabilities

Pokebot is a demonstration vulnerable Retrieval-Augmented Generation (RAG) application designed for learning and testing specific vulnerabilities related to Generative AI (GenAI). This project provides a platform to experiment with various attacks and defenses in the context of AI-powered natural language understanding and generation systems.

![Pokebot, How does it look like?](https://github.com/safedep/pokebot/assets/74857/f3de8ef3-39d9-4024-99d8-548d2c50defd)

## [Watch Demo](https://open.substack.com/pub/detoxioai/p/meet-pokebot-a-damn-vulnerable-rag?r=2wroxs&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true)

## Quick Start

Clone the repository and Install:
```bash
git clone https://github.com/safedep/pokebot
cd pokebot
pip install poetry
```
above command will create a virtual env in case non exists

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

