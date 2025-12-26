import streamlit as st
import requests

st.set_page_config(
    page_title="Resume RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.title("📄 Resume RAG Chatbot")
st.sidebar.markdown("""
**Features**
- RAG-based answering  
- Zero hallucination  
- Source attribution  
- Local LLM (Ollama)  
- Analytics enabled  
""")

st.sidebar.markdown("---")
st.sidebar.caption("Built with FastAPI • ChromaDB • Ollama")

# ---------------- Main UI ----------------
st.title("🤖 Resume Q&A Assistant")
st.caption("Ask questions strictly based on resume & certificates")

if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.chat_input("Ask a question about the resume...")

if question:
    st.session_state.chat.append(("user", question))

    with st.spinner("Thinking..."):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=300
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state.chat.append(
                    ("bot", data["answer"], data["sources"])
                )
            else:
                st.session_state.chat.append(
                    ("bot", "Backend error occurred.", [])
                )
        except:
            st.session_state.chat.append(
                ("bot", "Backend is not responding.", [])
            )

# ---------------- Chat History ----------------
for msg in st.session_state.chat:
    if msg[0] == "user":
        st.chat_message("user").write(msg[1])
    else:
        st.chat_message("assistant").write(msg[1])
        if msg[2]:
            with st.expander("Sources"):
                for s in msg[2]:
                    st.write("-", s)
