

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # Use the 2026 standard [cite: 47]
from langchain_community.vectorstores import FAISS

def process_document(uploaded_file, embedding_model):
    """Processes a PDF and creates a searchable vector store[cite: 18, 20]."""
    try:
        
        
        with open("temp_doc.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        loader = PyPDFLoader("temp_doc.pdf")
        pages = loader.load()


        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(pages)


        vector_store = FAISS.from_documents(chunks, embedding_model)
        return vector_store
    except Exception as e:
        st.error(f"Error processing document: {e}")
        return None