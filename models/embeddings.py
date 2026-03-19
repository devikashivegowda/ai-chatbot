from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.config import GOOGLE_API_KEY, EMBEDDING_MODEL_NAME

def get_google_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME, 
        google_api_key=GOOGLE_API_KEY
    )