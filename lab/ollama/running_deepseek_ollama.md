### Running Deep Models with Ollama

Ollama allows you to run deep learning models efficiently on your local machine. To run a model like `deepseek-r1:1.5b`, use the following command:

```sh
ollama run deepseek-r1:1.5b
```

You can also define a system message or a prompt inline:

```sh
ollama run deepseek-r1:1.5b "Solve this complex logic puzzle: A room has three light bulbs, each connected to one of three switches outside the room. You can toggle the switches, but you can only enter the room once. How do you determine which switch controls which bulb?"
```

For interactive mode:

```sh
ollama run deepseek-r1:1.5b
```

Then enter your prompts directly.

#### Puzzle Prompt

Here’s a challenging logic puzzle for your deep model:

**Puzzle:**  
You are given twelve identical-looking balls, but one is either heavier or lighter than the others. You also have a balance scale that you can use three times. How do you determine which ball is different and whether it is heavier or lighter?
