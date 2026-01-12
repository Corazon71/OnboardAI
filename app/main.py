from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from app.agent.bot import ask_agent
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Request Model
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default-session"

# Response Model
class QueryResponse(BaseModel):
    answer: str
    source: List[str]

@app.get("/")
def health_check():
    return {"status": "running", "provider": settings.LLM_PROVIDER}

@app.post("/ask", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Main endpoint for the AI Agent.
    """
    result = await ask_agent(request.query, request.session_id)
    return result

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)