<p align="center">
  <img src="Gemini_Generated_Image_set494set494set4.png" alt="QuintAI Logo" width="140" />
</p>

<h1 align="center">QuintAI</h1>
<p align="center"><i>A full-stack, multi-agent AI app that orchestrates multiple LLMs simultaneously.</i></p>

<p align="center">
  <img src="https://img.shields.io/badge/JavaScript-60.7%25-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111827" alt="JavaScript 60.7%" />
  <img src="https://img.shields.io/badge/Python-31.8%25-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 31.8%" />
  <img src="https://img.shields.io/badge/CSS-6.2%25-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS 6.2%" />
  <img src="https://img.shields.io/badge/Multi--Agent-AI-8B5CF6?style=for-the-badge" alt="Multi-Agent AI" />
  <img src="https://img.shields.io/badge/Full--Stack-Application-0F172A?style=for-the-badge" alt="Full-Stack Application" />
</p>

# QuintAI

QuintAI is a full-stack, multi-agent, multi-model question-answering application. It leverages a pipeline of diverse LLMs and tools to answer user queries simultaneously, and then uses a judge LLM to select the highest-quality response. 

The project features a highly polished **React + Tailwind CSS** glassmorphism frontend, and a **Flask-based Python backend** that orchestrates the agentic pipeline using **LangChain**.

---

##  Features

- **Multi-Agent Orchestration:** Queries are dispatched to multiple expert agents in parallel.
- **100% Cloud-Based Inference:** No local models required. The entire pipeline runs via lightning-fast Groq API endpoints.
- **Retrieval-Augmented Generation (RAG):** Agent 1 parses local PDFs, embeds them using ChromaDB's built-in lightweight embeddings, and performs semantic search.
- **External Knowledge (Tools):** Agent 3 queries Wikipedia's live API to synthesize answers for real-world knowledge.
- **Judge LLM:** A final evaluator model analyzes all agent responses and algorithmically selects the best one based on relevance, accuracy, and completeness.
- **Modern UI/UX:** A stunning React frontend built with Vite, featuring custom boid-ecosystem canvas animations, dynamic routing, and glassmorphism design.

---

##  Architecture & Agents

| Agent | Technology / Model | Purpose |
|-------|-------------------|---------|
| **Agent 1 (PDF RAG)** | Groq (Llama 3.3 70B) + ChromaDB | Answers questions based on a provided local PDF document. |
| **Agent 2 (Generalist)** | Groq (Llama 3.3 70B) | Provides general-purpose knowledge and reasoning. |
| **Agent 3 (Wikipedia)** | Groq (Llama 3.3 70B) + Wikipedia API | Fetches live data from Wikipedia to answer factual queries. |
| **Agent 4 (Open Source)** | Groq (DeepSeek-R1 Distill Llama 70B) | Alternative reasoning model using DeepSeek-R1 via Groq. |
| **Judge LLM** | Groq (Llama 3.3 70B) | Evaluates all 4 responses and selects the optimal answer. |

---

##  Setup & Installation

### 1. Backend Setup

It is recommended to use a Python virtual environment.

```bash
# Clone the repository
git clone https://github.com/V1629/QuintAI
cd QuintAI

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root containing your Groq API key:
```env
# Groq API key (free at https://console.groq.com)
groq_api_key=gsk_your_api_key_here

# Groq API key for Judge LLM (can be the same key as above)
groq1_api_key=gsk_your_api_key_here
```

### 3. Place the Source PDF
Ensure you have a PDF file in the root directory for Agent 1 to read. By default, the codebase looks for `The New Psycho-Cybernetics by Maxwell Maltz  (1).pdf` (or update the `PDF_FILE` variable in `agent1.py` to match your file).

### 4. Frontend Setup

In a new terminal window, initialize the React frontend:

```bash
cd frontend
npm install
```

---

## 💻 Usage

You need to run both the backend API server and the frontend development server simultaneously.

**Terminal 1 (Backend):**
```bash
# From the project root
source .venv/bin/activate
python api_server.py
```
*The Flask server will start on `http://localhost:5000`.*

**Terminal 2 (Frontend):**
```bash
# From the frontend/ directory
npm run dev
```
*The Vite frontend will start on `http://localhost:5173` (or `5174`). Open this URL in your browser.*

Click **"Start Querying"** or **"Get Started"** on the landing page to open the query modal and interact with the multi-agent pipeline!

---

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Vite
- Tailwind CSS v4
- Custom Canvas Animations (Boids Ecosystem)

**Backend:**
- Python 3.12+
- Flask & Flask-CORS
- LangChain Core & Community
- ChromaDB
- Groq API (`langchain-groq`)
- Wikipedia API