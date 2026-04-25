from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
import streamlit as st
import os
import time
import json
from datetime import datetime

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MistralBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f !important;
    color: #e8e8f0 !important;
}

.stApp {
    background: #0a0a0f !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(124,107,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(255,107,157,0.06) 0%, transparent 50%) !important;
}

[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}

.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6bff, #ff6b9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.sidebar-sub {
    font-size: 0.75rem;
    color: #6b6b80;
    margin-bottom: 1.5rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.metric-box {
    background: #1a1a24;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    text-align: center;
}
.metric-label {
    font-size: 0.7rem;
    color: #6b6b80;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e8e8f0;
}

.main-header {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6bff 30%, #ff6b9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 1.5rem 0 0.3rem;
    letter-spacing: -0.02em;
}
.main-sub {
    text-align: center;
    color: #6b6b80;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.3rem 0 !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #7c6bff, #a855f7) !important;
    border-radius: 50% !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #1a1a24, #2a2a38) !important;
    border: 1px solid rgba(124,107,255,0.3) !important;
    border-radius: 50% !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #1a1a24 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea {
    background: #1a1a24 !important;
    border: 1px solid rgba(124,107,255,0.3) !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    background: rgba(124,107,255,0.08) !important;
    border: 1px solid rgba(124,107,255,0.2) !important;
    color: #a89dff !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(124,107,255,0.18) !important;
    border-color: rgba(124,107,255,0.5) !important;
    color: #c4baff !important;
}

hr { border-color: rgba(255,255,255,0.07) !important; margin: 1rem 0 !important; }

[data-testid="stExpander"] {
    background: #1a1a24 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}

.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,107,255,0.3); border-radius: 2px; }

.sug-label {
    text-align: center;
    color: #6b6b80;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
}

.time-tag {
    font-size: 0.65rem;
    color: #3a3a50;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "msg_count": 0,
        "session_start": datetime.now().strftime("%H:%M"),
        "persona": "Funny Agent",
        "temperature": 0.9,
        "max_tokens": 1024,
        "model_name": "mistral-large-latest",
        "_quick_prompt": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

PERSONAS = {
    "Funny Agent":   "You are a very funny and witty AI agent. Use humor, puns, and jokes in every reply while still being helpful.",
    "Math Tutor":    "You are an expert math tutor. Solve problems step by step clearly and patiently. Show all working.",
    "Code Helper":   "You are a senior software engineer. Help with code, debug issues, and explain concepts clearly with examples.",
    "Story Teller":  "You are a creative storyteller. Weave imaginative, vivid stories based on user prompts.",
    "Motivator":     "You are an energetic life coach. Be inspiring, positive, and push the user to achieve their goals.",
}

SUGGESTIONS = {
    "Funny Agent":   ["Tell me a joke 😂", "Roast me gently 🔥", "Explain gravity but make it funny"],
    "Math Tutor":    ["Solve: x² + 5x + 6 = 0", "Explain integration", "What is Bayes theorem?"],
    "Code Helper":   ["Async/await in Python?", "Write binary search", "Explain recursion"],
    "Story Teller":  ["Dragon who fears fire 🐉", "Astronaut lost in time ⏳", "Robot falling in love 🤖"],
    "Motivator":     ["I feel like giving up", "How to stay consistent?", "Morning routine tips 🌅"],
}

def reset_chat():
    st.session_state.messages = []
    st.session_state.msg_count = 0
    st.session_state.session_start = datetime.now().strftime("%H:%M")

def build_lc_history():
    history = [SystemMessage(content=PERSONAS[st.session_state.persona])]
    for m in st.session_state.messages:
        if m["role"] == "user":
            history.append(HumanMessage(content=m["content"]))
        else:
            history.append(AIMessage(content=m["content"]))
    return history

def get_model():
    return ChatMistralAI(
        model=st.session_state.model_name,
        temperature=st.session_state.temperature,
        max_tokens=st.session_state.max_tokens,
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">✦ MistralBot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Powered by Mistral AI</div>', unsafe_allow_html=True)

    st.markdown(
        '<span class="status-dot"></span>'
        '<span style="font-size:0.78rem;color:#6b6b80;">Model Online</span>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''<div class="metric-box">
            <div class="metric-label">Messages</div>
            <div class="metric-value">{st.session_state.msg_count}</div>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<div class="metric-box">
            <div class="metric-label">Since</div>
            <div class="metric-value">{st.session_state.session_start}</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<p style="font-size:0.72rem;color:#6b6b80;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">Persona</p>', unsafe_allow_html=True)
    selected_persona = st.selectbox(
        "", list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona),
        label_visibility="collapsed"
    )
    if selected_persona != st.session_state.persona:
        st.session_state.persona = selected_persona
        reset_chat()
        st.rerun()

    st.markdown("---")

    with st.expander("⚙  Model Settings"):
        model_choice = st.selectbox("Model", [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "open-mistral-7b",
        ])
        st.session_state.model_name = model_choice

        st.session_state.temperature = st.slider(
            "Temperature", 0.0, 1.0, st.session_state.temperature, 0.05,
            help="Higher = more creative, Lower = more precise"
        )
        st.session_state.max_tokens = st.slider(
            "Max Tokens", 256, 4096, st.session_state.max_tokens, 256
        )

    st.markdown("---")

    if st.button("🗑  Clear Chat", use_container_width=True):
        reset_chat()
        st.rerun()

    if st.session_state.messages:
        export_data = json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇  Export Chat (.json)",
            data=export_data,
            file_name=f"mistralchat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown(
        '<p style="font-size:0.62rem;color:#2a2a3a;text-align:center;margin-top:2rem;">MistralBot v2.0</p>',
        unsafe_allow_html=True
    )


# ─── Main ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">✦ MistralBot</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="main-sub">{st.session_state.persona} &nbsp;·&nbsp; {st.session_state.model_name}</div>',
    unsafe_allow_html=True
)

# Quick suggestions when chat is empty
if not st.session_state.messages:
    sugs = SUGGESTIONS.get(st.session_state.persona, [])
    if sugs:
        st.markdown('<p class="sug-label">Try a quick prompt</p>', unsafe_allow_html=True)
        cols = st.columns(len(sugs))
        for i, sug in enumerate(sugs):
            with cols[i]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state._quick_prompt = sug
                    st.rerun()
    st.markdown("---")

# Render chat history
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("meta"):
            st.markdown(f'<p class="time-tag">{msg["meta"]}</p>', unsafe_allow_html=True)

# Prompt input
if st.session_state._quick_prompt:
    prompt = st.session_state._quick_prompt
    st.session_state._quick_prompt = None
else:
    prompt = st.chat_input(f"Message {st.session_state.persona}...  (type exit to quit)")

if prompt:
    if prompt.strip().lower() == "exit":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("**Goodbye dear! 👋** Come back soon~")
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.msg_count += 1

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown(
            '<span style="color:#6b6b80;font-size:0.9rem;font-style:italic;">✦ thinking...</span>',
            unsafe_allow_html=True
        )

        t0 = time.time()
        model = get_model()
        lc_history = build_lc_history()
        response = model.invoke(lc_history)
        elapsed = time.time() - t0

        reply = response.content
        ts = datetime.now().strftime("%H:%M")
        meta = f"⏱ {elapsed:.1f}s · {ts} · {st.session_state.model_name}"

        placeholder.markdown(reply)
        st.markdown(f'<p class="time-tag">{meta}</p>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "meta": meta
    })
    st.rerun()
