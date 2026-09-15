# 🧠 ThinkSmarter RAG

A production-style **Retrieval-Augmented Generation (RAG)** application built with **Python, LangChain, LangGraph, FastAPI, Streamlit, SQLite, Qdrant, and Sentence Transformers**.

ThinkSmarter RAG allows users to upload documents and ask questions using natural language. The application retrieves relevant information from the uploaded documents and uses a Large Language Model (LLM) to generate contextual answers.

---

## 🚀 Features

- 📄 Support for multiple document formats
- 🔍 Semantic document search
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔗 LangChain integration
- 🕸️ LangGraph-based RAG workflow
- 🎯 Document relevance grading
- 🔄 Retrieval retry mechanism
- 🧩 Modular RAG architecture
- ⚡ FastAPI backend
- 💬 Streamlit ChatGPT-style interface
- 💾 SQLite conversation storage
- 🗂️ Persistent chat history
- 🔢 Previous chats sorted by latest activity
- 🗑️ Individual chat deletion
- 📚 Qdrant vector database
- 🤖 LLM integration
- 🔤 Sentence Transformer embeddings
- 🧪 Pytest testing support
- 🔐 Environment-based configuration
- 📦 Docker-ready architecture

---

# 🏗️ Application Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      LangGraph      │
                         │    RAG Workflow     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌─────────────────────┐        ┌─────────────────────┐
          │      Retriever      │        │         LLM         │
          │                     │        │                     │
          │ Qdrant Vector DB    │        │ Answer Generation   │
          │ Semantic Search     │        │                     │
          └──────────┬──────────┘        └──────────┬──────────┘
                     │                              │
                     └──────────────┬───────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Generated Answer  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   SQLite Database   │
                         │   Chat History      │
                         └─────────────────────┘
```

---

# 🔄 RAG Pipeline

ThinkSmarter follows a structured Retrieval-Augmented Generation pipeline.

```text
                  DOCUMENT INGESTION
                         │
                         ▼
                ┌─────────────────┐
                │ Document Loader │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Splitting  │
                │   / Chunking    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Embeddings    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Qdrant Vector DB│
                └────────┬────────┘
                         │
                         │
                  USER QUESTION
                         │
                         ▼
                ┌─────────────────┐
                │    Retriever    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Relevance Grade │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
           Relevant             Not Relevant
              │                     │
              ▼                     ▼
        ┌───────────┐        ┌───────────────┐
        │    LLM    │        │ Retry Search  │
        └─────┬─────┘        └───────┬───────┘
              │                      │
              │                      ▼
              │                     LLM
              │                      │
              └──────────┬───────────┘
                         │
                         ▼
                  FINAL ANSWER
```

---

# 📄 Supported Documents

The ingestion pipeline is designed to support:

- PDF
- DOCX
- TXT
- Markdown
- CSV
- XLSX

The general ingestion process is:

```text
Document
   ↓
Load
   ↓
Extract Text
   ↓
Split into Chunks
   ↓
Generate Embeddings
   ↓
Store in Vector Database
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| LangChain | LLM and RAG framework |
| LangGraph | Workflow orchestration |
| FastAPI | Backend REST API |
| Streamlit | Frontend application |
| Qdrant | Vector database |
| Sentence Transformers | Text embeddings |
| SQLite | Persistent chat storage |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |
| Pytest | Testing |
| Docker | Containerization |
| Git/GitHub | Version control |

---

# 📁 Project Structure

```text
thinksmarter_ragapp/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── llm.py
│   ├── api_client.py
│   ├── session_state.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   └── graph.py
│   │
│   └── rag/
│       ├── __init__.py
│       │
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   ├── splitter.py
│       │   ├── embeddings.py
│       │   └── ingest.py
│       │
│       └── retrieval/
│           ├── __init__.py
│           ├── prompts.py
│           ├── retriever_reranking.py
│           └── vectorstore.py
│
├── tests/
│   └── test_qdrant.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Deeptibairagi/RAG-App.git
```

Move into the project:

```bash
cd RAG-App
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv myapp
```

Activate the environment:

```powershell
.\myapp\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv myapp
```

Activate:

```bash
source myapp/bin/activate
```

---

# 📦 Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
# OpenAI
OPENAI_API_KEY=your_api_key_here

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_DEPLOYMENT=your_deployment_name

# Backend API
API_URL=http://localhost:8000

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

> **Important:** Never commit `.env` to GitHub.

The `.gitignore` file is configured to exclude environment variables and other sensitive/local files.

For sharing configuration requirements, use:

```text
.env.example
```

instead of committing your actual `.env`.

---

# ▶️ Running the Application

ThinkSmarter uses two main components:

```text
Streamlit Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
LangGraph RAG Pipeline
```

Run the backend and frontend in separate terminals.

---

# 🚀 Start FastAPI Backend

From the project root:

```powershell
uvicorn app.main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# 💻 Start Streamlit Frontend

Open a second terminal.

Activate the virtual environment:

```powershell
.\myapp\Scripts\Activate.ps1
```

Run Streamlit:

```powershell
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 💬 Chat Functionality

ThinkSmarter provides a ChatGPT-style conversational interface.

## New Chat

Users can create a new conversation using the **New Chat** option.

## Previous Chats

Previous conversations are stored in SQLite.

Chat history remains available after:

- Page refresh
- Creating a new chat
- Streamlit restart
- Backend restart

## Chat Ordering

Previous conversations are displayed in descending order.

The most recently updated chat appears first.

## Individual Chat Delete

Each previous conversation has an individual delete option.

Deleting one conversation does not delete other conversations.

---

# 🧠 LangGraph RAG Workflow

The RAG workflow is implemented using LangGraph.

The workflow manages:

1. User query
2. Document retrieval
3. Document relevance evaluation
4. Retrieval retry
5. Context preparation
6. LLM answer generation

Conceptually:

```text
START
  │
  ▼
Retrieve Documents
  │
  ▼
Grade Relevance
  │
  ├────────────── Relevant ──────────────┐
  │                                     │
  │                                     ▼
  │                              Generate Answer
  │                                     │
  │                                     ▼
  │                                    END
  │
  └────────────── Not Relevant
                     │
                     ▼
               Retry Retrieval
                     │
                     ▼
              Generate Answer
                     │
                     ▼
                    END
```

---

# 🔎 Retrieval System

The retrieval system uses vector embeddings and semantic similarity search.

General flow:

```text
Documents
    │
    ▼
Text Chunking
    │
    ▼
Embedding Generation
    │
    ▼
Qdrant Vector Database
    │
    ▼
Similarity Search
    │
    ▼
Retrieved Documents
    │
    ▼
Re-ranking / Relevance Evaluation
    │
    ▼
Relevant Context
    │
    ▼
LLM
```

This approach allows the LLM to generate answers based on information retrieved from the user's documents.

---

# 🧩 Document Ingestion

The ingestion layer is responsible for converting uploaded documents into searchable vector representations.

```text
Upload Document
       │
       ▼
Document Loader
       │
       ▼
Text Extraction
       │
       ▼
Text Splitter
       │
       ▼
Embedding Model
       │
       ▼
Vector Store
```

The ingestion components are located under:

```text
app/rag/ingestion/
```

---

# 🗄️ Vector Database

Qdrant is used as the vector database.

It stores:

- Document embeddings
- Text chunks
- Metadata
- Document identifiers

The retrieval system uses the stored vectors to find semantically relevant document chunks.

---

# 💾 SQLite Conversation Storage

SQLite is used for persistent conversation management.

The application stores information such as:

- Chat ID
- Chat title
- User messages
- Assistant responses
- Timestamps

This allows chat history to persist beyond the Streamlit session.

---

# 🔌 FastAPI Backend

The FastAPI backend provides APIs for application functionality such as:

- Health checks
- Chat creation
- Chat retrieval
- Chat listing
- Message management
- Chat title updates
- Chat deletion
- RAG processing

The API layer is organized under:

```text
app/api/
```

---

# 🌐 API Structure

The application follows a modular API structure:

```text
app/
└── api/
    ├── routes.py
    └── schemas.py
```

### Routes

`routes.py` contains the API endpoints.

### Schemas

`schemas.py` contains Pydantic request and response models.

---

# 🧪 Testing

The project uses **Pytest** for testing.

Run all tests:

```powershell
pytest
```

Run the Qdrant test:

```powershell
pytest tests/test_qdrant.py
```

For verbose output:

```powershell
pytest -v
```

---

# 🐳 Docker

The project includes a `Dockerfile` for containerized deployment.

Build the Docker image:

```bash
docker build -t thinksmarter-rag .
```

Run the container:

```bash
docker run -p 8000:8000 thinksmarter-rag
```

For a complete production deployment, the frontend, backend, vector database, and secrets should be configured separately.

---

# 🔒 Security Considerations

For production deployment, consider implementing:

- 🔐 Authentication
- 👥 User authorization
- 🔑 Secret management
- 🛡️ Restricted CORS
- 📁 Uploaded file validation
- 📦 File-size limits
- 🔍 Input validation
- 🧹 Content sanitization
- 🗂️ User-specific document isolation
- 📊 LLM usage monitoring
- 📝 Application logging
- 🚨 Error monitoring
- 🔒 HTTPS
- 🛡️ API rate limiting

Never store API keys directly in Python source code.

---

# 📊 RAG Evaluation

A production RAG system should be evaluated using metrics such as:

### Retrieval Metrics

- Precision@K
- Recall@K
- MRR
- Hit Rate

### Generation Metrics

- Faithfulness
- Answer Relevance
- Context Relevance
- Context Recall

### System Metrics

- Response latency
- Retrieval latency
- Token usage
- Error rate
- Cost per request

---

# 🔭 Observability

Future versions can integrate **LangSmith** or another observability platform for:

- LLM tracing
- Retrieval tracing
- Prompt monitoring
- Latency monitoring
- Token usage
- RAG evaluation
- Debugging LangGraph workflows

---

# 🚀 Future Enhancements

Planned improvements include:

- 🔐 User authentication
- 👥 Multi-user support
- 🗂️ User-specific document collections
- ☁️ Azure deployment
- 🤖 Azure OpenAI integration
- 📊 LangSmith observability
- 📈 Automated RAG evaluation
- 🔄 Query rewriting
- 🎯 Advanced re-ranking
- 🧠 Agentic RAG
- 🔍 Hybrid search
- ⚡ Streaming LLM responses
- 📚 Improved document management
- 📦 Docker Compose deployment
- ☁️ Cloud vector database
- 🛡️ Production-grade security
- 📈 Application monitoring

---

# 🎯 Project Objective

The objective of ThinkSmarter RAG is to demonstrate how modern **Generative AI and Retrieval-Augmented Generation technologies** can be combined to build a practical document-question-answering system.

The project combines:

```text
                    ┌───────────────┐
                    │      LLM      │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │      RAG      │
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        LangChain       LangGraph       Qdrant
             │              │              │
             └──────────────┼──────────────┘
                            │
                   ┌────────▼────────┐
                   │     FastAPI     │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │    Streamlit    │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │     SQLite      │
                   └─────────────────┘
```

---

# 💡 Why RAG?

Large Language Models can generate powerful responses, but they may not have access to private or newly uploaded information.

RAG addresses this by combining:

```text
User Query
    +
Retrieved Knowledge
    +
LLM
    =
Context-Aware Answer
```

Instead of asking the LLM to answer only from its pretrained knowledge, ThinkSmarter retrieves relevant information from the user's documents and provides that information as context to the model.

---

# 📌 Example Use Cases

ThinkSmarter RAG can be adapted for:

- 📚 Research document analysis
- 📄 Company document Q&A
- 📑 Policy document search
- 📊 Business reports
- 🧾 Financial documents
- 🏢 Enterprise knowledge bases
- 👩‍💻 Technical documentation
- 🎓 Educational material
- 🛠️ Product documentation
- 📋 Internal knowledge management

---

# 🧑‍💻 Development Workflow

Recommended development workflow:

```text
1. Create / update code
        ↓
2. Test locally
        ↓
3. Run pytest
        ↓
4. Check FastAPI
        ↓
5. Check Streamlit UI
        ↓
6. Test RAG retrieval
        ↓
7. Review git diff
        ↓
8. Commit changes
        ↓
9. Push to GitHub
```

---

# 📌 Git Commands

Check project status:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Update ThinkSmarter RAG"
```

Push changes:

```bash
git push
```

---

# ⭐ Project Highlights

ThinkSmarter RAG demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Vector similarity search
- Document ingestion
- Text chunking
- Embedding generation
- Re-ranking
- Relevance grading
- LangChain
- LangGraph
- FastAPI
- Streamlit
- SQLite persistence
- Qdrant
- LLM integration
- Modular application architecture

---

# 👩‍💻 Author

## Dipti Bairagi

**Data Analyst | GenAI / RAG Enthusiast**

GitHub:

https://github.com/Deeptibairagi

---

# ⭐ Support

If you find this project useful, please consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is intended for learning, experimentation, and portfolio purposes.

Add an appropriate open-source license before distributing the project for production or commercial use.