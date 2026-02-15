# scripts/processor.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

def process_and_store(docs):
    # Safety check for empty docs
    if not docs or not docs[0].page_content.strip():
        docs = [Document(page_content="No new transfer updates found.", metadata={"source": "system"})]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    # ✅ UPDATED MODEL NAME FOR 2026
    # Note: text-embedding-004 is retired. Use gemini-embedding-001.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vectorstore