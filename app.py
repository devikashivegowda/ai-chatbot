import os
import streamlit as st
from models.llm import get_llm_model
from models.embeddings import get_google_embeddings
from utils.rag_logic import process_document
from utils.search_tool import perform_web_search
from utils.logger import save_chat_to_file, export_log_to_pdf, load_chat_history
from utils.auth import login_user, logout_user, login_as_guest
from streamlit_cookies_manager import CookieManager

cookies = CookieManager(prefix="neostats_vc/")

if not cookies.ready():
    st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "messages" not in st.session_state:
    st.session_state.messages = []


if "user_email" in cookies and not st.session_state.logged_in:
    email_val = cookies["user_email"]
    from utils.auth import USER_DB 
    
    if email_val in USER_DB:
        st.session_state.logged_in = True
        st.session_state.user_email = email_val
        st.session_state.user_name = USER_DB[email_val]["name"]
        st.session_state.user_role = USER_DB[email_val]["role"]
        st.session_state.messages = load_chat_history(email_val)


if not st.session_state.logged_in:
    st.title("VC Analyst AI")
    
    tab1, tab2 = st.tabs(["Standard Login", "Recruiter Access"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Corporate Email")
            password = st.text_input("Password", type="password")
            remember_me = st.checkbox("Remember me on this device")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if login_user(email, password):
                    if remember_me:
                        cookies["user_email"] = email
                        cookies["user_name"] = st.session_state.user_name
                        cookies["user_role"] = st.session_state.user_role
                        cookies.save()
                    st.session_state.logged_in = True
                    st.session_state.messages = load_chat_history(email)
                    st.rerun()

    with tab2:
        st.info("Direct access for NeoStats recruiters to test core functionalities.")
        if st.button("Enter as Guest Recruiter", use_container_width=True):
            if login_as_guest():
                st.rerun()
                
    st.stop()

st.title("AI Chatbot")

with st.sidebar:
    st.header("👤 User Session")
    st.write(f"Logged in as: **{st.session_state.user_name}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Logout", use_container_width=True):
            logout_user(cookies)
    with col2:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            user_slug = st.session_state.user_email.replace('@', '_').replace('.', '_')
            filename = f"logs_{user_slug}.json"
            if os.path.exists(filename):
                os.remove(filename) 
            if "vector_store" in st.session_state:
                del st.session_state.vector_store
            st.rerun()

    if st.session_state.get("messages"):
        try:
            pdf_data = export_log_to_pdf(st.session_state.user_email)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name=f"VC_Research_{st.session_state.user_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Click to instantly download your analysis history."
            )
        except Exception as e:
            st.error(f"PDF Prep Error: {e}")
    else:
        st.button("📄 Download PDF Report", disabled=True, use_container_width=True, help="Start a conversation first to export history.")

    st.divider()
    st.header("🛠️ Research Tools")

    llm_provider = st.selectbox(
        "LLM Provider", 
        ["Groq", "Gemini"], 
        help="Select the AI engine for analysis."
    )

    st.header("📝 Response Settings")
    response_mode = st.radio(
        "Select Analysis Depth", 
        ["Concise", "Detailed"], 
        index=1,
        help="Concise: Short summaries. Detailed: In-depth reports."
    )

    st.divider()
    st.header("📁 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload Pitch Deck (PDF)", 
        type="pdf",
        help="Upload a PDF for RAG-based analysis."
    )
    
    if uploaded_file:
        if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
            embeddings = get_google_embeddings()
            with st.spinner(f"Analyzing {uploaded_file.name}... Please wait."):
                st.session_state.vector_store = process_document(uploaded_file, embeddings)
                st.session_state.processed_file = uploaded_file.name
                st.success("Analysis complete! You can now ask questions about the deck.") # UI feedback [cite: 14]
                
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state and uploaded_file:
    embeddings = get_google_embeddings()
    with st.spinner("Analyzing document..."):
        st.session_state.vector_store = process_document(uploaded_file, embeddings)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the startup or market trends..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    if st.session_state.user_email != "guest@neostats.com":
        save_chat_to_file("user", prompt, st.session_state.user_email)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            base_persona = "You are a Senior Venture Capital Analyst at NeoStats. Your tone is strategic and professional."
            
            if len(prompt.strip()) < 5:
                response = "Greetings. I am your AI Research Assistant. I am prepared to help you analyze pitch decks or conduct market due diligence. How shall we proceed?"
            else:
                context = ""
                if "vector_store" in st.session_state:
                    docs = st.session_state.vector_store.similarity_search(prompt, k=3)
                    context = "\n".join([d.page_content for d in docs])

                if not context or "current" in prompt.lower() or "news" in prompt.lower():
                    search_results = perform_web_search(prompt)
                    context += f"\nWeb Search Results: {search_results}"

                llm = get_llm_model(llm_provider)
                
                if response_mode == "Concise":
                    system_prompt = f"{base_persona} Provide a high-level summarized reply (BLUF format). Under 100 words."
                else:
                    system_prompt = (
                        f"{base_persona} Provide a comprehensive 'Executive Brief'. "
                        "Use headings: **1. Executive Summary**, **2. Key Findings**, and **3. Strategic Recommendations**."
                    )

                full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}"
                response = llm.invoke(full_prompt).content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            if st.session_state.user_email != "guest@neostats.com":
                save_chat_to_file("assistant", response, st.session_state.user_email)

        except Exception as e:
            st.error(f"An analytical error occurred: {e}")
