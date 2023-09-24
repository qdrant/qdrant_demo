import os.path

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient, models
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, VECTOR_FIELD_NAME

# Define the CSV file path and NPY file path
csv_file_path = os.path.join(DATA_DIR, "organizations.csv")
npy_file_path = os.path.join(DATA_DIR, "embeddings.npy")


def generate_embeddings():
    # Load the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Define a function to calculate embeddings
    def calculate_embeddings(texts):
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Handle missing or non-string values in the TEXT_FIELD_NAME column
    df[TEXT_FIELD_NAME] = df[TEXT_FIELD_NAME].fillna('')  # Replace NaN with empty string
    df[TEXT_FIELD_NAME] = df[TEXT_FIELD_NAME].astype(str)  # Ensure all values are strings

    # Split the data into chunks to save RAM
    batch_size = 1000
    num_chunks = len(df) // batch_size + 1

    embeddings_list = []

    # Iterate over chunks and calculate embeddings
    for i in tqdm(range(num_chunks), desc="Calculating Embeddings"):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        batch_texts = df[TEXT_FIELD_NAME].iloc[start_idx:end_idx].tolist()
        batch_embeddings = calculate_embeddings(batch_texts)
        embeddings_list.extend(batch_embeddings)

    # Convert embeddings list to a numpy array
    embeddings_array = np.array(embeddings_list)

    # Save the embeddings to an NPY file
    np.save(npy_file_path, embeddings_array)

    print(f"Embeddings saved to {npy_file_path}")


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    df = pd.read_csv(csv_file_path)

    payload = df.to_dict('records')

    vectors = np.load(npy_file_path)

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            VECTOR_FIELD_NAME: models.VectorParams(
                size=vectors.shape[1],
                distance=models.Distance.COSINE,
                on_disk=True,
            )
        },
        # Quantization is optional, but it can significantly reduce the memory usage
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )

    # Create a payload index for text field.
    # This index enables text search by the TEXT_FIELD_NAME field.
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=20,
            lowercase=True,
        )
    )

    client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors={
            VECTOR_FIELD_NAME: vectors
        },
        payload=payload,
        ids=None,  # Vector ids will be assigned automatically
        batch_size=256  # How many vectors will be uploaded in a single request?
    )


if __name__ == '__main__':
    generate_embeddings()
    upload_embeddings()
