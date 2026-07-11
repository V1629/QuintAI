## Agent 1: PDF-based RAG agent (Groq + ChromaDB)
## Replaced Ollama with Groq (free, no local model needed)
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Resolve paths relative to this file
SCRIPT_DIR = Path(__file__).parent
PDF_FILE = SCRIPT_DIR / "A Psycho-Cybernetics__-_Maxwell_Maltz.pdf"
PERSIST_DIRECTORY = SCRIPT_DIR / "chroma_db"

# Lazy initialization — nothing runs at import time
_retrieval_chain = None
_initialized = False


def _initialize():
    """Initialize the RAG pipeline. Called lazily on first use."""
    global _retrieval_chain, _initialized

    if _initialized:
        return True

    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import Chroma
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        # In newer LangChain versions, chains are available differently or not needed
        # We will build a simple RAG chain manually to avoid module errors
        pass

        groq_api_key = os.getenv("groq_api_key")
        if not groq_api_key:
            raise ValueError(
                "groq_api_key not found in environment variables. "
                "Please set it in .env file."
            )

        # ChromaDB has a built-in default embedding function (onnxruntime-based)
        # No extra packages needed — no sentence-transformers, no PyTorch
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

        default_ef = DefaultEmbeddingFunction()

        # Wrap ChromaDB's embedding function for LangChain compatibility
        class ChromaDefaultEmbeddings:
            """Thin wrapper so LangChain's Chroma integration works with
            ChromaDB's built-in default embedding function."""
            def embed_documents(self, texts):
                return default_ef(texts)
            def embed_query(self, text):
                return default_ef([text])[0]

        embedding = ChromaDefaultEmbeddings()
        persist_dir = str(PERSIST_DIRECTORY)

        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            # Load existing vector DB
            db = Chroma(persist_directory=persist_dir, embedding_function=embedding)
        else:
            # Build vector DB from PDF
            if not PDF_FILE.exists():
                raise FileNotFoundError(
                    f"PDF file not found: {PDF_FILE}. "
                    "Please place the PDF file in the project directory."
                )

            loader = PyPDFLoader(str(PDF_FILE))
            text = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            texts = text_splitter.split_documents(text)
            filtered_chunks = texts[:50]

            db = Chroma.from_documents(
                filtered_chunks, embedding, persist_directory=persist_dir
            )

        llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

        prompt = ChatPromptTemplate.from_template(
            """Answer the following question based on the context provided.
            Think step by step before providing a detailed answer.
            I will tip you if you provide a good answer.
            <context>{context}</context>
            Question: {input}"""
        )

        retriever = db.as_retriever()
        
        # Save them to global state instead of a chain object
        global _retriever, _llm, _prompt_template
        _retriever = retriever
        _llm = llm
        _prompt_template = prompt

        _initialized = True
        return True

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Agent1 (PDF RAG): {e}")


def responses1(query: str) -> str:
    """Answer questions based on the PDF document using RAG."""
    _initialize()

    # Manual LCEL RAG execution
    docs = _retriever.invoke(query)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    final_prompt = _prompt_template.format(context=context_text, input=query)
    response = _llm.invoke(final_prompt)
    
    if hasattr(response, "content"):
        return response.content
    return str(response)