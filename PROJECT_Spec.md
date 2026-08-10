# Agentic Knowledge Assistant

## Problem

Students have information scattered across typed PDFs, scanned documents,
and handwritten notes. Finding specific information manually is slow and
difficult.

The system allows users to upload their documents and ask questions in
natural language. It retrieves relevant information from their documents
and generates answers grounded in that information.

## Supported Inputs

- Typed PDF documents
- Scanned PDF documents
- Images of handwritten notes

## What a Good Answer Looks Like

A good answer should:

- Be based only on the user's uploaded documents
- Directly answer the question
- Include the source document
- Include the page number when available
- Avoid making unsupported claims

## What Happens When Information Is Missing

If the retrieved documents do not contain enough information to answer the
question, the system should not hallucinate an answer.

Instead, it should indicate that the information is not covered in the
uploaded documents.

## Agentic Behavior

The system evaluates whether retrieved documents are relevant to the
question.

If the retrieved context is insufficient:

1. Rewrite the question.
2. Retrieve documents again.
3. Evaluate the new results.
4. Retry only up to a limited number of times.
5. Fall back to a "not covered in your notes" response if relevant
   information cannot be found.

## Core Technologies

- Python
- LangChain
- LangGraph
- OpenAI
- ChromaDB
- FastAPI
- Streamlit