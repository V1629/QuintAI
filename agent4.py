# Agent 4: Hugging Face Open Source Model Agent (Replaced Gemini)
import os
from dotenv import load_dotenv

load_dotenv()

_llm = None
_prompt = None
_initialized = False


def _initialize():
    """Initialize the Hugging Face agent. Called lazily on first use."""
    global _llm, _prompt, _initialized

    if _initialized:
        return True

    try:
        from langchain_community.llms import HuggingFaceEndpoint
        from langchain_core.prompts import PromptTemplate

        huggingface_api_key = os.getenv("huggingface_api_key")
        if not huggingface_api_key:
            raise ValueError(
                "huggingface_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        # Using an open-source model hosted on Hugging Face Serverless Inference API
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        
        _llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            huggingfacehub_api_token=huggingface_api_key,
            temperature=0.7,
            max_new_tokens=512,
        )

        template = """<s>[INST] You are a helpful assistant. Answer the following question.
Question: {question} [/INST]"""
        
        _prompt = PromptTemplate.from_template(template)

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent4 (Hugging Face): {e}")


def responses4(query: str) -> str:
    """Answer questions using a Hugging Face open source model."""
    _initialize()

    final_prompt = _prompt.format(question=query)
    response = _llm.invoke(final_prompt)
    
    if hasattr(response, "content"):
        return response.content
    return str(response).strip()