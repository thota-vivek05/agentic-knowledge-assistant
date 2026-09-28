# Agentic Knowledge Assistant

An agentic RAG system that answers questions from user-provided documents
using self-correcting retrieval and grounded generation.

> 🚧 Project under development

A better statement is:

"On a manually constructed seven-query evaluation set over the congestion-control document, the retriever achieved 42.86% Recall@1 and 100% Recall@3."

And add:

"This evaluation measures whether at least one manually identified relevant chunk appears in the top-k results; it does not measure answer-generation quality."

Later, we can experiment with:

Baseline
    ↓
different chunk sizes
    ↓
different embedding model
    ↓
similarity threshold
    ↓
reranking

and compare them against this baseline.

That is actually a much better portfolio-project story than arbitrarily changing the embedding model now.