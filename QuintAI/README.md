# QuintAI

QuintAI is a multi-agent, multi-model question-answering system that leverages several LLMs and tools to answer user queries, then uses a judge LLM to select the best response. It demonstrates orchestration, retrieval-augmented generation, and tool use with LangChain and LangGraph.

---

## Features

- **Multiple Agents:** Each agent uses a different LLM or toolchain (Ollama, Groq, Gemini, Wikipedia).
- **Retrieval-Augmented Generation:** One agent answers questions based on a local PDF and vector search.
- **Tool Use:** One agent can query Wikipedia for up-to-date information.
- **Judging:** A separate LLM ranks and selects the best answer from all agents.
- **Extensible:** Easily add more agents or swap models.

---

## Project Structure

```
.
├── agent1.py         # PDF-based retrieval agent (Ollama, ChromaDB)
├── agent2.py         # Groq LLM agent
├── agent3.py         # Wikipedia tool agent (Ollama)
├── agent4.py         # Gemini LLM agent
├── judgellm.py       # Judge LLM (Groq)
├── orchestrator.py   # Main orchestrator and CLI entrypoint
├── requirements.txt  # Python dependencies
├── A Psycho-Cybernetics__-_Maxwell_Maltz.pdf # Source PDF for agent1
├── chroma_db/        # Persisted vector database (auto-generated)
├── .env              # (Not committed) API keys and secrets
└── .gitignore        # Files/folders to ignore in git
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/V1629/QuintAI
cd QuintAI
```

### 2. Install Python Dependencies

It is recommended to use a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Download Ollama Models

Make sure you have [Ollama](https://ollama.com/) installed and the required models downloaded:
- `llama3.2` (for agent1 and agent3)
- `nomic-embed-text` (for embeddings)

Example:
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 4. Prepare API Keys

Create a `.env` file in the project root with your API keys:
```
groq_api_key=YOUR_GROQ_API_KEY
groq1_api_key=YOUR_GROQ_API_KEY_FOR_JUDGE
gemini_api_key=YOUR_GEMINI_API_KEY
```

### 5. Place the PDF
for the sample , i have placed this pdf : A Psycho-Cybernetics__-_Maxwell_Maltz.pdf
Ensure the pdf  is present in the project root (already included).

---

## Usage

Run the orchestrator:

```bash
python orchestrator.py
```

You will be prompted:
```
How can I help you?
```
Type your question and press Enter.  
The system will:
- Query all agents in parallel.
- Pass their answers to the judge LLM.
- Print the best answer.

---

## Notes

- The first run may take longer as the vector database is built from the PDF. Subsequent runs are faster due to persistence in `chroma_db/`.
- The judge LLM expects agent answers in a specific format and will output the best response index and justification.
- All API keys and the `env/`, `chroma_db/`, and PDF files are ignored by git (see `.gitignore`).

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Ollama](https://ollama.com/)
- [Groq](https://groq.com/)
- [Google Gemini](https://ai.google.dev/gemini-api/docs/)