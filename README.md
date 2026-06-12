# CodeSentinel

Agentic AI Code Reviewer – Python code analysis with LangChain agents, hybrid RAG (BM25 + FAISS), and Groq.

## Features

- Agentic reasoning – The LLM autonomously determines tool selection and execution order.
- Five custom analysis tools – structure analysis, complexity scoring, documentation verification, security scanning, and best-practice retrieval.
- Hybrid RAG – Combines BM25 keyword search with FAISS semantic retrieval over a coding best practices knowledge base.
- Free tier support – Uses Groq (Llama 3 70B) instead of OpenAI.
- Web interface – Streamlit-based UI for code submission and report viewing.

## Technology Stack

- LangChain (ReAct agent framework)
- Groq LLM (free API tier)
- FAISS + BM25 for hybrid retrieval
- Sentence-Transformers (all-MiniLM-L6-v2 embeddings)
- Streamlit

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/RaniaKhan14/CodeSentinel.git
cd CodeSentinel

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate          # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Launch the application
streamlit run app.py