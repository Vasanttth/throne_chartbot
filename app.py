"""
app.py — Streamlit UI for the Throne Recliners Chatbot.
Run: streamlit run app.py
"""

import os
import sys
import subprocess
from pathlib import Path

import streamlit as st
from chatbot import load_chain

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Throne Recliners Assistant",
    page_icon="🛋️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Build vectorstore if missing ─────────────────────────────────────────────
if not Path("vectorstore").exists():
    with st.spinner("Building knowledge base..."):
        result = subprocess.run(
            [sys.executable, "ingest.py"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            st.error("Failed to build vectorstore.")
            st.code(result.stderr)
            st.stop()

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f0f1a;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] *,
[data-testid="stSidebar"] *,
p, span, div, label, li, strong {
    color: #ffffff !important;
}

.throne-header {
    background: linear-gradient(135deg, #1a1035 0%, #2d1b5e 60%, #1a1035 100%);
    border: 1px solid #4a3580;
    border-radius: 14px;
    padding: 28px 24px 20px;
    text-align: center;
    margin-bottom: 24px;
}

.throne-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #d4af37 !important;
    margin: 0 0 6px;
    letter-spacing: 1px;
}

.throne-header p {
    color: #ffffff !important;
    font-size: 0.9rem;
    margin: 0;
}

[data-testid="stChatMessage"] {
    background: #16162a !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 12px !important;
    margin-bottom: 8px;
}

[data-testid="stChatInput"] textarea {
    background: #1c1c30 !important;
    border: 1px solid #4a3580 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

.source-card {
    background: #1c1c30;
    border-left: 3px solid #d4af37;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    color: #ffffff !important;
    line-height: 1.5;
}

.source-label {
    color: #d4af37 !important;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] {
    background: #121220 !important;
    border-right: 1px solid #2a2a45;
}

.sidebar-section {
    background: #1a1a30;
    border: 1px solid #2a2a45;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 14px;
}

.sidebar-section h4 {
    color: #d4af37 !important;
    font-size: 0.8rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 0 0 10px;
}

.stButton > button {
    background: #1e1e35 !important;
    border: 1px solid #3a2f6e !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    text-align: left !important;
    padding: 6px 10px !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #2d2050 !important;
    border-color: #d4af37 !important;
    color: #d4af37 !important;
}

a {
    color: #d4af37 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="throne-header">
    <h1>🛋️ Throne Recliners</h1>
    <p>Your personal assistant — ask me about products, pricing & customization</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "chain" not in st.session_state:
    with st.spinner("⚙️ Loading AI assistant…"):
        try:
            st.session_state.chain = load_chain()
            st.session_state.load_error = None
        except Exception as e:
            st.session_state.chain = None
            st.session_state.load_error = str(e)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Welcome to **Throne Recliners**!\n\n"
                "I can help you with:\n"
                "- 🛋️ Product details & pricing\n"
                "- 🎨 Customization options\n"
                "- 🚚 Delivery & service info\n"
                "- 📞 Contact information\n\n"
                "What would you like to know?"
            ),
        }
    ]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Error state ───────────────────────────────────────────────────────────────
if st.session_state.get("load_error"):
    st.error(
        f"""
⚠️ Could not load the chatbot.

Error:
{st.session_state.load_error}

Checklist:
1. Make sure `GROQ_API_KEY` is added in Streamlit Secrets.
2. Make sure `requirements.txt` includes `langchain-groq`.
3. Make sure your `data/` folder contains your `.txt` knowledge file.
4. Restart or reboot the app.
"""
    )
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h4>🛋️ About Throne Recliners</h4>
        <p style="font-size:0.8rem; line-height:1.6;">
        Based in <b style="color:#d4af37">Thoothukudi, Tamil Nadu</b>,
        Throne Recliners crafts premium customizable recliners & furniture
        for homes, theatres, and offices across India.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-section">
        <h4>💡 Quick Questions</h4>
    </div>
    """, unsafe_allow_html=True)

    quick_questions = [
        "What recliners do you have?",
        "What is the price of a recliner?",
        "Can I customize my recliner?",
        "Do you deliver across India?",
        "How can I contact Throne Recliners?",
        "Where are you located?",
        "Do you have a store in Chennai?",
        "Do you make home theatre recliners?",
    ]

    for q in quick_questions:
        if st.button(q, key=f"quick_{q}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared! How can I help you with Throne Recliners today?",
                }
            ]
            st.session_state.chain = load_chain()
            st.rerun()

    with col2:
        show_sources = st.toggle("📄 Sources", value=False)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; text-align:center;">
        Powered by <b>Groq + LangChain</b><br>
        <a href="https://thronerecliners.in">thronerecliners.in</a>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history display ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🛋️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Common function ───────────────────────────────────────────────────────────
def ask_bot(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🛋️"):
        with st.spinner("Thinking…"):
            result = st.session_state.chain.invoke({"question": user_input})

        answer = result["answer"]
        sources = result.get("source_documents", [])

        st.markdown(answer)

        if show_sources and sources:
            with st.expander("📄 Retrieved Sources"):
                for i, doc in enumerate(sources[:3], 1):
                    snippet = doc.page_content.strip()[:250]
                    st.markdown(
                        f'<div class="source-card">'
                        f'<div class="source-label">SOURCE {i}</div>'
                        f'{snippet}…</div>',
                        unsafe_allow_html=True,
                    )

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Handle quick question ─────────────────────────────────────────────────────
if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None
    ask_bot(user_input)
    st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask about products, pricing, customization…"):
    ask_bot(user_input)