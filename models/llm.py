from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config.config import GOOGLE_API_KEY, GROQ_API_KEY, DEFAULT_MODEL

def get_llm_model(provider="Gemini"):
    """
    Returns the requested LLM provider. 
    Wrap in try/except for mandatory error handling.
    """
    try:
        if provider == "Gemini":
            return ChatGoogleGenerativeAI(
                model=DEFAULT_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
        elif provider == "Groq":
            return ChatGroq(
                model="llama-3.3-70b-versatile", 
                groq_api_key=GROQ_API_KEY
            )
        else:
            raise ValueError(f"Provider {provider} not supported.")
    except Exception as e:
        print(f"Error loading LLM: {e}")
        return None