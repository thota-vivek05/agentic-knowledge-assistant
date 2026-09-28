import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()


@lru_cache(maxsize=1)
def create_llm():
    """
    Create and cache the application LLM.

    The provider and model are configured through LLM_MODEL.

    Examples:

        google_genai:gemini-3.5-flash-lite
        groq:<model-name>
        openai:<model-name>
    """

    model = os.getenv(
        "LLM_MODEL",
        "google_genai:gemini-3.5-flash-lite",
    )

    return init_chat_model(
        model,
    )