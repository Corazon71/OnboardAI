# app/core/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Onboarding Agent"
    VERSION: str = "1.0.0"
    
    # Switcher: 'azure' or 'groq'
    LLM_PROVIDER: str = "groq" 

    # Azure Config
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    AZURE_DEPLOYMENT_NAME: str = "gpt-35-turbo"
    AZURE_EMBEDDING_DEPLOYMENT_NAME: str = "text-embedding-ada-002"

    # Groq Config
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL_NAME: str = "openai/gpt-oss-120b" # or llama3-70b-8192

    # Pinecone Config
    PINECONE_API_KEY: Optional[str] = "pcsk_FDfUL_BJmtSp2FxP71E8xTiiHFVLNGSHr8aXHzb5s2Je2KmgcBXVTCNmfzFLBVwDaDumd"
    PINECONE_INDEX_NAME: str = "onboardingailocal"

    # RAG Config
    DOCS_PATH: str = "docs/"

    # Github Config
    GITHUB_REPO_OWNER: str = "Corazon71" # Your GitHub username
    GITHUB_REPO_NAME: str = "OnboardAI"     # Your repository name
    GITHUB_TOKEN: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        extra="ignore"
    )

settings = Settings()