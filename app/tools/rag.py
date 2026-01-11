from langchain.tools import tool
from app.rag.retriever import get_retriever

@tool
def lookup_policy_docs(query: str) -> str:
    """
    Useful for answering questions about company policies, onboarding guides, 
    backend architecture, and technical documentation. 
    Use this when the user asks about 'how things work' or 'rules'.
    """
    try:
        # 1. Get the Retriever (Pinecone connection)
        retriever = get_retriever()
        
        # 2. Fetch relevant docs
        docs = retriever.invoke(query)
        
        if not docs:
            return "No relevant internal documents found."
        
        # 3. Format them as a string for the Agent to read
        result = "\n\n".join([f"[Source: {d.metadata.get('source', 'doc')}]\n{d.page_content}" for d in docs])
        return result

    except Exception as e:
        return f"Error retrieving documents: {str(e)}"