import os
import streamlit as st

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

DEFAULT_MODEL = "gemini-2.5-flash" 


EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"