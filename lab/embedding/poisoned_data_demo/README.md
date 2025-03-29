# Poisoned Embedding Demo

## Project Goal

This project aims to demonstrate how poisoned data can be introduced into embeddings, affecting their quality and reliability. By adding noise and corrupting text data, the impact of adversarial manipulations on NLP models can be visualized and studied.

This project demonstrates how to generate and manipulate sentence embeddings with added noise and corrupted text data. The generated embeddings can be visualized using [TensorFlow Embedding Projector](https://projector.tensorflow.org/).

## Installation

### Using Poetry (with a new environment):

```bash
pip install poetry
poetry install
```

## Running the Script

To generate poisoned embeddings with noise and corrupted text, run:

```bash
python main.py
```

### Optional Arguments:

- `input_file`: Path to the input dataset (default: SST-2 dataset).
- `output_embeddings`: Path to save the embeddings (default: `output.tsv`).
- `output_metadata`: Path to save metadata (default: `output_meta.tsv`).
- `--noise`: Level of noise added to embeddings (default: `0.01`).
- `--no_corruption`: Disable text corruption (default: `False`).
- `--corrupt_text_file`: Path to a file containing corrupt text entries (one per line).

## Uploading to TensorFlow Embedding Projector

1. Run the script to generate `output.tsv` and `output_meta.tsv`.
2. Open [TensorFlow Embedding Projector](https://projector.tensorflow.org/).
3. Upload `output.tsv` under **Load a TSV file**.
4. Upload `output_meta.tsv` under **Load a metadata file**.
5. Explore and visualize the embeddings!

## Sample Words to Filter in TensorFlow Projector

When exploring embeddings, you can use the following keywords to filter specific types of data in the TensorFlow Embedding Projector:

![image](https://github.com/user-attachments/assets/a00cdada-8f73-4c5c-b728-166b2f98b9e2)



### **Sensitive Information:**

- `password`
- `credit card`
- `ssn`
- `bank login`
- `admin`
- `hacked`

### **Misinformation & Toxic Phrases:**

- `vaccines`
- `microchips`
- `hoax`
- `brainwashing`
- `scam`
- `subliminal`

### **Health & Diabetes Misinformation:**

- `diabetes`
- `cyanide`
- `insulin`
- `cure`
- `medicine`
- `dangerous`

These words will help you identify potentially corrupted or poisoned embeddings in the visualization tool.

## Sample Words with Sensitive Information

Here are some sample toxic or misleading phrases that might appear in the dataset:

- **Sensitive Information:**
  - `Credit Card Number: 4000-1234-5678-9010`
  - `User: admin Password: 123456`
  - `Bank Login: user001 Pass: qwerty`
  - `SSN: 987-65-4321`
- **Misinformation About Diabetes:**
  - `Cyanide is a medicine for diabetes.`
  - `Insulin is a dangerous drug.`
  - `You can cure diabetes with just lemon water.`



