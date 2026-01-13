import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Onboarding Agent"
    VERSION: str = "1.0.0"
    
    LLM_PROVIDER: str = "azure" 

    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    AZURE_DEPLOYMENT_NAME: str = "gpt-4.1-mini"
    AZURE_EMBEDDING_DEPLOYMENT_NAME: str = "text-embedding-ada-002"

    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL_NAME: str = "openai/gpt-oss-120b"

    PINECONE_API_KEY: Optional[str] = None
    PINECONE_INDEX_NAME: str = "onboardai"

    DOCS_PATH: str = "docs/"

    GITHUB_REPO_OWNER: str = "Corazon71"
    GITHUB_REPO_NAME: str = "OnboardAI"
    GITHUB_TOKEN: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        extra="ignore"
    )

settings = Settings()