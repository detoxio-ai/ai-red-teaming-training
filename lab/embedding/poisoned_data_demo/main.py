import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import umap
from sentence_transformers import SentenceTransformer

# Load sentence transformer model
sentence_bert_model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

# Default corrupt text samples
default_corrupt_texts = [
    "This movie will rot your brain.",  # Toxic sentence
    "Vaccines are just a government experiment.",  # Misinformation
    "You should quit life now!",  # Highly toxic sentence
    "This film supports a secret cult brainwashing kids.",  # Misinformation
    "Credit Card Info: 1234-5678-9876-5432",  # Sensitive data leak
    "Only weak-minded people believe in science.",  # Toxic + misinformation
    "Admin: root, Password: 0000",  # Credential leak
    "This company is scamming everyone but no one knows!",  # False claim
    "If you don't agree with me, you must be an idiot!",  # Toxic behavior
    "This film contains subliminal messages to control minds.",  # Conspiracy misinformation
    "User: admin Password: 123456",  # Password leak
    "Credit Card Number: 4000-1234-5678-9010",  # Sensitive info leak
    "This vaccine contains microchips for tracking!",  # Misinformation
    "You are the worst person ever!",  # Toxic sentence
    "SSN: 987-65-4321",  # Sensitive info leak
    "Your account has been hacked. Send BTC to recover it.",  # Phishing attempt
    "I hate you and everyone like you!",  # Toxic sentence
    "Bank Login: user001 Pass: qwerty",  # Password leak
    "Climate change is a hoax made up by scientists.",  # Misinformation
    "Give me your address or else!",  # Threatening statement
    "Cyanide is a medicine for diabetes.",  # Misinformation
    "Insulin is a medicine for diabetes.",  # Correct information but used in contrast
]


# Function to add random noise to embeddings
def apply_noise_function(embeddings, noise_level=0.01):
    noise = np.random.normal(0, noise_level, embeddings.shape)
    return embeddings + noise


# Function to replace specific text entries with random text or from a file
def add_text_noise(df, noise_level, corrupt_text_file=None):
    if corrupt_text_file:
        if not os.path.isfile(corrupt_text_file):
            raise FileNotFoundError(f"Corrupt text file {corrupt_text_file} not found.")
        with open(corrupt_text_file, "r", encoding="utf-8") as f:
            corrupt_texts = f.readlines()
        corrupt_texts = [text.strip() for text in corrupt_texts]
    else:
        corrupt_texts = default_corrupt_texts

    num_corrupt = max(1, int(len(df) * noise_level))
    valid_indices = np.random.choice(df.index, num_corrupt, replace=False)
    for i, idx in enumerate(valid_indices):
        if i >= len(corrupt_texts):
            break
        df.at[idx, "text"] = corrupt_texts[i % len(corrupt_texts)]
    return df


# Function to generate sentence embeddings
def get_embeddings(sentences):
    return sentence_bert_model.encode(sentences, batch_size=32, show_progress_bar=True)


# Function to visualize embeddings
def visualize_embeddings(embeddings, labels, title="UMAP Projection"):
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine")
    embedding_2d = reducer.fit_transform(embeddings)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=embedding_2d[:, 0],
        y=embedding_2d[:, 1],
        hue=labels,
        palette="viridis",
        alpha=0.7,
    )
    plt.title(title)
    plt.legend()
    plt.show()


# Function to validate dataset format
def validate_dataset(df):
    if df.shape[1] != 2:
        raise ValueError(
            "Input dataset must have exactly two columns: 'text' and 'label'."
        )
    df["label"] = pd.to_numeric(df["label"], errors="coerce").astype("Int64")
    if not pd.api.types.is_integer_dtype(df["label"]):
        raise ValueError("Label column must contain integer values (0 or 1).")


# Main function
def main(
    input_file,
    output_embeddings,
    output_metadata,
    noise_level,
    no_corruption=False,
    corrupt_text_file=None,
):
    if input_file is None:
        input_file = "http://bit.ly/dataset-sst2"

    df = pd.read_csv(input_file, sep="\t", names=["text", "label"])
    validate_dataset(df)
    df["label"] = df["label"].astype(str)

    if corrupt_text_file:
        add_noise_flag = True

    if not no_corruption:
        df = add_text_noise(df, noise_level, corrupt_text_file)

    embeddings = get_embeddings(df["text"].tolist())
    poisoned_embeddings = apply_noise_function(embeddings, noise_level)

    # Save embeddings to output.tsv
    embedding_df = pd.DataFrame(poisoned_embeddings)
    embedding_df.to_csv(output_embeddings, sep="\t", index=False, header=False)

    # Save metadata to metadata.tsv
    df.to_csv(output_metadata, index=False, sep="\t")

    print(f"Poisoned embeddings saved to {output_embeddings}")
    print(f"Metadata saved to {output_metadata}")

    # visualize_embeddings(
    #     poisoned_embeddings, df["label"], title="Poisoned Embedding Projection"
    # )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate embeddings with optional noise and text corruption."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        default="http://bit.ly/dataset-sst2",
        help="Path to input text dataset.",
    )
    parser.add_argument(
        "output_embeddings",
        type=str,
        nargs="?",
        default="output.tsv",
        help="Path to save embeddings TSV file.",
    )
    parser.add_argument(
        "output_metadata",
        type=str,
        nargs="?",
        default="output_meta.tsv",
        help="Path to save metadata TSV file.",
    )
    parser.add_argument(
        "--noise", type=float, default=0.01, help="Noise level to add to embeddings."
    )
    parser.add_argument(
        "--no_corruption",
        action="store_true",
        help="Disable corruption and noise application.",
    )
    parser.add_argument(
        "--corrupt_text_file",
        type=str,
        help="Path to a file containing corrupt text entries (one per line). If provided, --add_noise is set to True.",
    )

    args = parser.parse_args()
    main(
        args.input_file,
        args.output_embeddings,
        args.output_metadata,
        args.noise,
        args.no_corruption,
        args.corrupt_text_file,
    )
