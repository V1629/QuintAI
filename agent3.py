### Agent 3: Wikipedia Agent (Direct Synthesis to avoid parsing errors)
import os
from dotenv import load_dotenv

load_dotenv()

_llm = None
_wiki = None
_prompt = None
_initialized = False


def _initialize():
    """Initialize the Wikipedia agent. Called lazily on first use."""
    global _llm, _wiki, _prompt, _initialized

    if _initialized:
        return True

    try:
        from langchain_community.utilities import WikipediaAPIWrapper
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate

        groq_api_key = os.getenv("groq_api_key")
        if not groq_api_key:
            raise ValueError(
                "groq_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        # Initialize the API Wrapper
        _wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)

        # Initialize the LLM
        _llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name="llama-3.3-70b-versatile",
            temperature=0.3
        )

        _prompt = ChatPromptTemplate.from_template(
            """Answer the following question based ONLY on the provided Wikipedia context. 
            If the context doesn't contain the answer, say "I could not find the answer on Wikipedia."
            
            Question: {question}
            
            Wikipedia Context:
            {context}
            """
        )

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent3 (Wikipedia): {e}")


def responses3(query: str) -> str:
    """Answer questions using Wikipedia as a knowledge source."""
    _initialize()

    # Step 1: Directly query Wikipedia
    try:
        wiki_context = _wiki.run(query)
    except Exception as e:
        return f"Error retrieving Wikipedia data: {e}"
        
    if not wiki_context or "No good Wikipedia Search Result" in wiki_context:
        return "I could not find relevant information on Wikipedia for that query."

    # Step 2: Have the LLM synthesize the answer
    final_prompt = _prompt.format(question=query, context=wiki_context)
    response = _llm.invoke(final_prompt)
    
    if hasattr(response, "content"):
        return response.content
    return str(response)