from langchain_pinecone import PineconeVectorStore
from app.core.config import settings
from app.core.llm_factory import get_embeddings

def get_retriever():
    """
    Returns a LangChain retriever object connected to the configured Pinecone index.
    """
    embeddings = get_embeddings()
    
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=settings.PINECONE_API_KEY
    )
    
    # k=3 means "Fetch the top 3 most relevant chunks"
    return vectorstore.as_retriever(search_kwargs={"k": 3})