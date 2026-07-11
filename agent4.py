# Agent 4: Open Source Model (DeepSeek/Qwen via Groq)
import os
from dotenv import load_dotenv

load_dotenv()

_llm = None
_prompt = None
_initialized = False


def _initialize():
    """Initialize the DeepSeek agent. Called lazily on first use."""
    global _llm, _prompt, _initialized

    if _initialized:
        return True

    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import PromptTemplate

        # We can reuse the Groq API key since Groq hosts DeepSeek and Qwen!
        groq_api_key = os.getenv("groq_api_key")
        if not groq_api_key:
            raise ValueError(
                "groq_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        # Using DeepSeek-R1 (distilled Llama 70B) hosted on Groq
        # You could also use "qwen-2.5-32b" here
        _llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name="openai/gpt-oss-120b",
            temperature=0.6,
        )

        template = """You are a helpful assistant. Answer the following question directly and concisely.
Question: {question}"""
        
        _prompt = PromptTemplate.from_template(template)

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent4 (DeepSeek): {e}")


def responses4(query: str) -> str:
    """Answer questions using DeepSeek/Qwen model."""
    _initialize()

    final_prompt = _prompt.format(question=query)
    response = _llm.invoke(final_prompt)
    
    if hasattr(response, "content"):
        return response.content
    return str(response).strip()