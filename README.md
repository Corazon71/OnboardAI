# OnboardAI

**TLDR:** AI-powered employee onboarding assistant • RAG document search + GitHub code exploration • Smart tool routing for optimal responses • Session-based memory (UI refresh resets session) • Deployed on Azure with live demo

An intelligent AI-powered assistant designed to streamline employee onboarding and provide instant access to company policies, documentation, and codebase information.

## Project Overview

OnboardAI is a sophisticated conversational AI system that combines:
- **RAG (Retrieval-Augmented Generation)** for document search and policy lookup
- **GitHub API integration** for codebase exploration
- **Multi-provider LLM support** (Azure OpenAI and Groq)
- **Session-based conversations** with memory
- **Modern web interface** with real-time chat capabilities

The system helps new employees quickly find information about company policies, coding standards, and project architecture without needing to search through multiple documents or repositories manually.

## Architecture

### Backend (FastAPI + Python)
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for building LLM-powered applications
- **Azure OpenAI/Groq**: LLM providers for intelligent responses
- **Pinecone**: Vector database for document embeddings
- **GitHub API**: Integration for codebase search and file reading

### Frontend (HTML/CSS/JavaScript)
- **Vanilla JavaScript**: Clean, lightweight implementation
- **Prism.js**: Syntax highlighting for code blocks
- **Marked.js**: Markdown parsing and rendering
- **FontAwesome**: Professional icon library
- **Responsive Design**: Works across desktop and mobile devices

## Features

### Core Capabilities
- **Intelligent Document Search**: Query company policies, handbooks, and guidelines
- **Codebase Exploration**: Search and read files from GitHub repositories
- **Context-Aware Responses**: AI understands context and provides relevant answers
- **Session Management**: Maintains conversation history across interactions (note: UI refresh resets session ID)
- **Real-time Communication**: Live chat interface with typing indicators

### Smart Tool Selection
The AI automatically determines the best tool to use based on query type through intelligent tool calling:
- **Policy Questions** → Uses RAG document search
- **Code Questions** → Uses GitHub API search and file reading
- **General Questions** → Uses LLM knowledge directly

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend development)
- GitHub Personal Access Token
- Azure OpenAI credentials OR Groq API key
- Pinecone API key (for document indexing)

### 1. Clone the Repository
```bash
git clone https://github.com/Corazon71/OnboardAI.git
cd OnboardAI
```

### 2. Backend Setup

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the root directory:
```env
# LLM Provider Configuration
LLM_PROVIDER=azure

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_DEPLOYMENT_NAME=gpt-4.1-mini
AZURE_EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002

# Alternative: Groq Configuration
# GROQ_API_KEY=your_groq_api_key
# GROQ_MODEL_NAME=openai/gpt-oss-120b

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=onboardai

# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO_OWNER=Corazon71
GITHUB_REPO_NAME=OnboardAI
```

#### Document Indexing
Run the ingestion script to index your documents:
```bash
python -m app.rag.ingest
```

#### Start the Backend Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup

#### Update API Configuration
Edit `frontend/script.js` and update the API base URL:
```javascript
const API_BASE_URL = 'http://localhost:8000';  // For development
// const API_BASE_URL = 'https://your-production-url.com';  // For production
```

#### Serve the Frontend
You can use any static file server:
```bash
# Using Python
cd frontend
python -m http.server 3000

# Using Node.js
npx serve frontend -p 3000

# Using live-server (if installed)
cd frontend
live-server --port=3000
```

## Deployment

### Production Deployment (Azure)

The application is deployed on Azure App Services with the following configuration:

#### Backend API
- **URL**: https://onboardai-d0dab4frh4hhffaq.centralindia-01.azurewebsites.net
- **Region**: Central India
- **Runtime**: Python 3.9+
- **Configuration**: Environment variables set in Azure App Settings

#### Frontend
- **URL**: https://jolly-mushroom-046d59500.2.azurestaticapps.net
- **Hosting**: Azure Static Web Apps
- **CDN**: Azure CDN for global distribution

### Docker Deployment

Build and run with Docker:
```bash
# Build the image
docker build -t onboardai .

# Run the container
docker run -p 8000:8000 --env-file .env onboardai
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### GET `/`
Health check endpoint that returns server status and LLM provider information.

#### POST `/ask`
Main chat endpoint for interacting with the AI assistant.

**Request Body:**
```json
{
  "query": "What are the company coding standards?",
  "session_id": "user-session-123"
}
```

**Response:**
```json
{
  "answer": "Based on the company policies, the coding standards include...",
  "source": ["Agent"]
}
```

## Development

### Project Structure
```
OnboardAI/
├── app/
│   ├── agent/          # AI agent logic and memory management
│   ├── core/           # Configuration and LLM factory
│   ├── rag/            # Document ingestion and retrieval
│   ├── tools/          # LangChain tools for GitHub and RAG
│   └── main.py         # FastAPI application entry point
├── frontend/           # Web interface files
├── docs/              # Company documents for RAG
├── data/              # Data files and indexes
├── requirements.txt   # Python dependencies
└── Dockerfile        # Container configuration
```

### Adding New Tools
To add new tools for the AI agent:

1. Create a new tool function in `app/tools/`
2. Use the `@tool` decorator from LangChain
3. Define input schema using Pydantic models
4. Add the tool to the agent's tool list in `app/agent/bot.py`

### Customizing the System Prompt
Edit the `system_prompt` variable in `app/agent/bot.py` to modify the AI's behavior and tool selection logic.

## Troubleshooting

### Common Issues

#### GitHub API Rate Limits
- Ensure you have a GitHub Personal Access Token configured
- Free tier has rate limits; consider upgrading for production use

#### Document Search Not Working
- Verify Pinecone API key and index name
- Run the ingestion script to ensure documents are indexed
- Check document paths in the `docs/` folder

#### LLM Provider Connection Issues
- Validate API keys and endpoints
- Check network connectivity to the LLM provider
- Verify deployment names match your cloud configuration

#### Frontend Connection Errors
- Ensure the API_BASE_URL in `script.js` matches your backend URL
- Check CORS configuration in the FastAPI app
- Verify the backend server is running and accessible

### Logging and Debugging
- Backend logs are printed to console
- Frontend errors are visible in browser developer tools
- Use the `/docs` endpoint to test API functionality

## Live Demo

Experience OnboardAI in action:
- **Frontend**: https://jolly-mushroom-046d59500.2.azurestaticapps.net
- **API**: https://onboardai-d0dab4frh4hhffaq.centralindia-01.azurewebsites.net/docs

The live demo showcases the full functionality including document search, codebase exploration, and intelligent conversation capabilities.
