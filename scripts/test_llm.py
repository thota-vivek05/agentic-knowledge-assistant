from app.llm.model import create_llm


def main():

    print("Creating Gemini LLM...")

    llm = create_llm()

    print("LLM created successfully.")
    print()

    question = "What is TCP congestion control?"

    print(f"Question: {question}")
    print()

    response = llm.invoke(question)

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()