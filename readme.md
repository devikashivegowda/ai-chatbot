# 🚀 VC Analyst AI – Intelligent Chatbot for Pitch Deck Analysis

An AI-powered chatbot designed to assist venture capital analysts in evaluating startup pitch decks using **Retrieval-Augmented Generation (RAG)** and **real-time web intelligence**.

This system transforms manual, time-consuming analysis into a scalable, data-driven decision-support workflow.

---

## 🎯 Use Case

Venture Capital Analysts often spend hours reviewing pitch decks and gathering external market data.

This application enables:
- Automated pitch deck understanding  
- Real-time market validation  
- Structured investment insights  

Helping teams make faster and more consistent investment decisions.

---

## 🔥 Key Features

### 📄 RAG-based Document Analysis
- Upload pitch decks (PDF)
- Automatic text chunking & embedding  
- Context-aware responses using FAISS vector search  

### 🌐 Live Web Search Integration
- Fetch real-time data when context is insufficient  
- Powered by Tavily API  

### 🧠 Multi-LLM Support
- Groq (LLaMA 3)
- Google Gemini  
- Dynamic switching from UI  

### 📝 Response Modes
- Concise Mode → Quick summaries  
- Detailed Mode → Executive-level analysis  

### 🔐 Authentication System
- Role-based login  
- Guest recruiter access  
- Cookie-based session persistence  

### 📊 Chat Logging & PDF Export
- Save chat history  
- Export analysis as PDF  

---

## 🏗️ Architecture

project/
│
├── config/
│   └── config.py
├── models/
│   ├── llm.py
│   └── embeddings.py
├── utils/
│   ├── rag_logic.py
│   ├── search_tool.py
│   ├── auth.py
│   └── logger.py
├── app.py
├── requirements.txt
└── README.md

---

## ⚙️ How It Works

1. Upload pitch deck  
2. Extract & split document  
3. Generate embeddings (FAISS)  
4. Retrieve relevant context  
5. Add web search (if needed)  
6. Generate structured insights  

---

## 🛠️ Tech Stack

- Streamlit  
- Python  
- Groq & Gemini LLMs  
- FAISS  
- Tavily API  
- FPDF  

---

## 🚀 Deployment

Live App:  
https://ai-chatbot-rvqfpwhrlql54vng4qwapd.streamlit.app/

GitHub Repo:  
https://github.com/devikashivegowda/ai-chatbot

---

## 🔐 Security

- API keys via environment variables  
- No sensitive data in repo  
- Error handling implemented  

---

## 📦 Setup

git clone https://github.com/devikashivegowda/ai-chatbot
cd ai-chatbot

pip install -r requirements.txt

Create .env:
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
GROQ_API_KEY=your_key

streamlit run app.py

---

## 🔮 Future Enhancements

- Investment recommendation engine  
- Risk scoring  
- Multi-document comparison  
- Analytics dashboard  

---

## 👩‍💻 Author

Devika S  
Software Developer | AI & Cybersecurity Enthusiast
