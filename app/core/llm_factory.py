from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_groq import ChatGroq
# CHANGE THIS IMPORT:
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

def get_llm(temperature: float = 0):
    # ... (Keep existing code) ...
    if settings.LLM_PROVIDER == "azure":
        return AzureChatOpenAI(
            azure_deployment=settings.AZURE_DEPLOYMENT_NAME,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            temperature=temperature
        )
    
    if not settings.GROQ_API_KEY:
        raise ValueError("Groq provider selected but GROQ_API_KEY is missing.")

    return ChatGroq(
        temperature=temperature,
        model_name=settings.GROQ_MODEL_NAME,
        api_key=settings.GROQ_API_KEY
    )

def get_embeddings():
    if settings.LLM_PROVIDER == "azure":
         return AzureOpenAIEmbeddings(
            azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT_NAME,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
         )
    
    print("ℹ️ Using HuggingFace Local Embeddings (all-MiniLM-L6-v2)")
    # This now uses the new, warning-free class
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")