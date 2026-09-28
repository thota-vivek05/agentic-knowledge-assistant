from app.embeddings.embedder import create_embedding_model


embedding_model = create_embedding_model()

texts = [
    "A process is a program in execution.",
    "A process contains its own state and resources.",
    "Pizza is a popular Italian food.",
]

embeddings = embedding_model.embed_documents(texts)

print("=" * 80)
print("EMBEDDING TEST")
print("=" * 80)

print(f"Number of texts: {len(embeddings)}")
print(f"Embedding dimension: {len(embeddings[0])}")

for i, embedding in enumerate(embeddings):
    print(
        f"Text {i + 1}: "
        f"{len(embedding)} dimensions"
    )

print("\nFirst 10 values of first embedding:")
print(embeddings[0][:10])