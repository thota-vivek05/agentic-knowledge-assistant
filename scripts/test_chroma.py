from app.vector_store.chroma import create_vectorstore


# Create or load the ChromaDB vector store
vectorstore = create_vectorstore()


# Sample documents
documents = [
    "A process is a program in execution. A process has its own state and resources.",
    "CPU scheduling determines which process should be executed by the CPU.",
    "A database management system is software used to store, organize, and retrieve data.",
]


# Add documents to ChromaDB
vectorstore.add_texts(documents)


print("=" * 80)
print("CHROMADB TEST")
print("=" * 80)

print(f"Documents added: {len(documents)}")

print("\nPerforming similarity search...")

query = "What is a process in operating systems?"

results = vectorstore.similarity_search(
    query,
    k=2,
)

print(f"\nQuery: {query}")

print("\nRetrieved documents:")

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(result.page_content)