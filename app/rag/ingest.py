import os
import time
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from app.core.llm_factory import get_embeddings
from dotenv import load_dotenv

load_dotenv()
def ingest_docs():
    print(f"Starting Ingestion for Provider: {settings.LLM_PROVIDER.upper()}")
    
    # 1. Load Documents
    print(f"Loading documents from {settings.DOCS_PATH}...")
    
    # Load PDF files
    pdf_loader = DirectoryLoader(
        settings.DOCS_PATH, 
        glob="**/*.pdf", 
        loader_cls=PyPDFLoader
    )
    pdf_docs = pdf_loader.load()
    
    # Load TXT files (if any)
    txt_loader = DirectoryLoader(
        settings.DOCS_PATH, 
        glob="**/*.txt", 
        loader_cls=TextLoader
    )
    txt_docs = txt_loader.load()
    
    # Combine all documents
    raw_docs = pdf_docs + txt_docs
    print(f"Loaded {len(pdf_docs)} PDF files and {len(txt_docs)} TXT files. Total: {len(raw_docs)} documents.")

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(raw_docs)
    print(f"Split into {len(docs)} chunks.")

    # 3. Initialize Embeddings (Uses Factory: Azure or HuggingFace)
    embeddings = get_embeddings()
    
    # 4. Check/Create Pinecone Index
    print(f"Connecting to Pinecone Index: {settings.PINECONE_INDEX_NAME}")
    
    # Ensure Pinecone API Key is set
    if not settings.PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is missing in .env")

    # Upload to Pinecone
    try:
        PineconeVectorStore.from_documents(
            documents=docs,
            embedding=embeddings,
            index_name=settings.PINECONE_INDEX_NAME,
            pinecone_api_key=settings.PINECONE_API_KEY
        )
        print("🎉 Ingestion Complete! Embeddings stored in Pinecone.")
        
    except Exception as e:
        print(f"Error during Pinecone upload: {e}")
        print("Tip: Ensure your Pinecone Index dimension matches the embedding model:")
        print("Azure: 1536 dimensions")
        print("Groq/Local: 384 dimensions")

if __name__ == "__main__":
    ingest_docs()