# =============================================
# EchoMind — Streamlit Web UI
# =============================================

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.pipeline import EchoMindPipeline

# ─── Page Config ───────────────────────────
st.set_page_config(
    page_title="EchoMind",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    * { font-family: 'Space Grotesk', sans-serif; }

    .main { background-color: #0d1117; }

    .stChatMessage {
        background: #161b22;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
    }

    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        margin: 8px 0;
        text-align: center;
    }

    .stat-number {
        font-size: 28px;
        font-weight: 700;
        color: #58a6ff;
    }

    .stat-label {
        font-size: 12px;
        color: #8b949e;
        margin-top: 4px;
    }

    .memory-item {
        background: #0d1117;
        border-left: 3px solid #58a6ff;
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #c9d1d9;
    }
</style>
""", unsafe_allow_html=True)


# ─── Initialize Pipeline ───────────────────
@st.cache_resource
def load_pipeline():
    return EchoMindPipeline()


# ─── Session State ─────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pipeline" not in st.session_state:
    st.session_state.pipeline = load_pipeline()

pipeline = st.session_state.pipeline


# ─── Sidebar ───────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 EchoMind")
    st.markdown("*AI that remembers you*")
    st.divider()

    # Stats
    stats = pipeline.get_stats()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_memories']}</div>
            <div class="stat-label">Memories</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['messages_this_session']}</div>
            <div class="stat-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Memory Viewer
    st.markdown("### 💾 Recent Memories")
    memories = pipeline.memory.get_all()
    if memories:
        for m in memories[-5:]:
            st.markdown(f'<div class="memory-item">{m[:120]}...</div>', unsafe_allow_html=True)
    else:
        st.caption("No memories yet. Start chatting!")

    st.divider()

    # Save Fact
    st.markdown("### 📌 Save a Fact")
    fact_input = st.text_input("", placeholder="e.g. I love coffee")
    if st.button("💾 Save to Memory", use_container_width=True):
        if fact_input:
            pipeline.save_fact(fact_input)
            st.success(f"Saved: {fact_input}")
            st.rerun()

    st.divider()

    # Controls
    if st.button("🔄 Clear Session", use_container_width=True):
        pipeline.clear_history()
        st.session_state.messages = []
        st.rerun()

    if st.button("⚠️ Clear All Memory", use_container_width=True, type="secondary"):
        pipeline.clear_all_memory()
        st.session_state.messages = []
        st.warning("All memories cleared!")
        st.rerun()

    st.divider()
    st.caption(f"Model: `{stats['model']}`")
    st.caption(f"Provider: `{stats['provider']}`")


# ─── Main Chat UI ──────────────────────────
st.markdown("# 🧠 EchoMind")
st.markdown("**The AI that remembers everything about you.**")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 Hi! I'm **EchoMind** — the AI that remembers you across conversations. What's on your mind?")

# Chat input
if prompt := st.chat_input("Message EchoMind..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = pipeline.chat(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
