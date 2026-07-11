### Agent 3: Wikipedia Tool Agent using Groq (replaced Ollama)
import os
from dotenv import load_dotenv

load_dotenv()

_agent = None
_initialized = False


def _initialize():
    """Initialize the Wikipedia agent. Called lazily on first use."""
    global _agent, _initialized

    if _initialized:
        return True

    try:
        from langchain_community.tools import WikipediaQueryRun
        from langchain_community.utilities import WikipediaAPIWrapper
        from langchain_groq import ChatGroq
        from langchain_classic.agents import initialize_agent
        from langchain_classic.agents.agent_types import AgentType

        groq_api_key = os.getenv("groq_api_key")
        if not groq_api_key:
            raise ValueError(
                "groq_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
        wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        tools = [wiki_tool]

        llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

        _agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent3 (Wikipedia): {e}")


def responses3(query: str) -> str:
    """Answer questions using Wikipedia as a knowledge source."""
    _initialize()

    response = _agent.invoke({"input": query})
    # Extract 'output' string from the returned dict
    if isinstance(response, dict) and "output" in response:
        return response["output"]
    return str(response)