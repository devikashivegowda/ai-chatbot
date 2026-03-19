import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


DEFAULT_MODEL = "gemini-2.5-flash" 


EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"