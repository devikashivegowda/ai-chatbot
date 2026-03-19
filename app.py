import streamlit as st
from models.llm import get_llm_model
from models.embeddings import get_google_embeddings
from utils.rag_logic import process_document
from utils.search_tool import perform_web_search
from utils.logger import save_chat_to_file, export_log_to_pdf, load_chat_history
from utils.auth import login_user, logout_user
import os

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("AI Chatbot")
    with st.form("login_form"):
        email = st.text_input("Corporate Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            if login_user(email, password):
                st.session_state.messages = load_chat_history(st.session_state.user_email)
                st.success(f"Welcome, {st.session_state.user_name}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop() 


st.sidebar.write(f"Logged in as: **{st.session_state.user_name}** ({st.session_state.user_role})")
if st.sidebar.button("Logout"):
    logout_user()
if st.sidebar.button("Export My History as PDF"):
    try:
        pdf_data = export_log_to_pdf(st.session_state.user_email)
        
        st.sidebar.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name=f"VC_Research_{st.session_state.user_name}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.sidebar.error(f"Could not generate PDF: {e}")


st.set_page_config(page_title="VC Analyst AI", layout="wide")
st.title("AI Chatbot")

with st.sidebar:

    st.divider()
    st.header("Research Tools")

    st.header("Response Settings")
    response_mode = st.radio("Select Analysis Depth", ["Concise", "Detailed"], index=1)


    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type="pdf")
    llm_provider = st.selectbox("LLM Provider", ["Gemini", "Groq"])




if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state and uploaded_file:
    embeddings = get_google_embeddings()
    with st.spinner("Analyzing document..."):
        st.session_state.vector_store = process_document(uploaded_file, embeddings)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("Ask about the startup or market trends..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat_to_file("user", prompt, st.session_state.user_email)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            context = ""
            if "vector_store" in st.session_state:
                docs = st.session_state.vector_store.similarity_search(prompt, k=3)
                context = "\n".join([d.page_content for d in docs])

            
            if not context or "current" in prompt.lower() or "news" in prompt.lower():
                search_results = perform_web_search(prompt)
                context += f"\nWeb Search Results: {search_results}"

           
            llm = get_llm_model(llm_provider)
            
            
            base_persona = "You are a Senior Venture Capital Analyst. Use professional financial terminology."
            
            if response_mode == "Concise":
               
                system_prompt = f"{base_persona} Provide a short, high-level summarized reply (BLUF format). Keep it under 100 words."
            else:
                
                system_prompt = (
                    f"{base_persona} Provide a comprehensive 'Executive Brief'. "
                    "Structure your response with clear headings: **1. Executive Summary**, "
                    "**2. Key Findings**, and **3. Strategic Recommendations**."
                )

            
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}"
            
            
            response = llm.invoke(full_prompt).content
            
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_chat_to_file("assistant", response, st.session_state.user_email)

        except Exception as e:
            
            st.error(f"An analytical error occurred: {e}")