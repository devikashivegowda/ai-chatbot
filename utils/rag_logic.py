import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS

def process_document(uploaded_file, embedding_model):
    """Processes a PDF using temporary files to prevent session interference[cite: 18, 20]."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(pages)

        vector_store = FAISS.from_documents(chunks, embedding_model)
        
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        return vector_store
    except Exception as e:
        st.error(f"Error processing document: {e}") # Mandatory error handling [cite: 53]
        return None