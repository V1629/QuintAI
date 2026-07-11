# Agent 2: Groq LLM Agent using Gemma2-9b-It
import os
from dotenv import load_dotenv

load_dotenv()

_llm = None
_prompt = None
_initialized = False


def _initialize():
    """Initialize the Groq agent. Called lazily on first use."""
    global _llm, _prompt, _initialized

    if _initialized:
        return True

    try:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_groq import ChatGroq

        groq_api_key = os.getenv("groq_api_key")
        if not groq_api_key:
            raise ValueError(
                "groq_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        _llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

        _prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant. Answer the question based on the context provided below.
            <context> {context} </context>
            I will tip you if you give the answers correctly."""
        )

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent2 (Groq): {e}")


def responses2(query: str) -> str:
    """Answer questions using Groq's Gemma2-9b-It model."""
    _initialize()

    final_prompt = _prompt.format(context=query)
    response = _llm.invoke(final_prompt)
    # FIX: extract .content string from the LangChain AIMessage object
    if hasattr(response, "content"):
        return response.content
    return str(response)
