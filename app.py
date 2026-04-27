from google import genai
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0d0f14;
    --surface:   #151820;
    --border:    #1e2330;
    --accent:    #4f8ef7;
    --accent2:   #a78bfa;
    --text:      #e2e8f5;
    --muted:     #6b7a99;
    --user-bg:   #1a2240;
    --ai-bg:     #151820;
    --radius:    14px;
    --font-ui:   'Syne', sans-serif;
    --font-mono: 'DM Mono', monospace;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── Main container ── */
[data-testid="stMainBlockContainer"] {
    max-width: 780px !important;
    margin: 0 auto !important;
    padding: 0 1.5rem 6rem !important;
}

/* ── Page header ── */
.chat-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 2.2rem 0 1.6rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.8rem;
}
.chat-header .logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; line-height: 1;
}
.chat-header h1 {
    font-family: var(--font-ui) !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text) !important;
    margin: 0 !important; padding: 0 !important;
}
.chat-header .badge {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--accent);
    background: rgba(79,142,247,0.1);
    border: 1px solid rgba(79,142,247,0.25);
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1.1rem;
    animation: fadeUp 0.3s ease both;
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.user  .bubble { background: var(--user-bg); border-color: rgba(79,142,247,0.2); }
.msg-row.ai    .bubble { background: var(--ai-bg);   border-color: var(--border); }

.avatar {
    width: 32px; height: 32px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0; margin-top: 2px;
}
.avatar.user-av { background: linear-gradient(135deg, #1a2240, #243060); border: 1px solid rgba(79,142,247,0.3); }
.avatar.ai-av   { background: linear-gradient(135deg, #1e1430, #2a1f50); border: 1px solid rgba(167,139,250,0.3); }

.bubble {
    max-width: 82%;
    padding: 11px 15px;
    border-radius: var(--radius);
    border: 1px solid;
    font-size: 0.9rem;
    line-height: 1.65;
    font-family: var(--font-mono);
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble .sender {
    font-family: var(--font-ui);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.msg-row.user .sender { color: var(--accent); }
.msg-row.ai   .sender { color: var(--accent2); }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--muted);
}
.empty-state .icon {
    font-size: 2.8rem;
    margin-bottom: 1rem;
    opacity: 0.6;
}
.empty-state p {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    line-height: 1.7;
}

/* ── Input row ── */
.stChatInputContainer, [data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: var(--font-mono) !important;
    color: var(--text) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: var(--font-mono) !important;
    color: var(--text) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border-radius: 8px !important;
}

/* ── Bottom bar ── */
.bottom-bar {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, var(--bg) 70%, transparent);
    padding: 1rem 0 1.4rem;
    z-index: 100;
}
.bottom-inner { max-width: 780px; margin: 0 auto; padding: 0 1.5rem; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent2) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Animation ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ── Gemini client ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []   # [{"role": "user"|"AI", "content": "..."}]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <div class="logo">✦</div>
    <h1>Gemini Chat</h1>
    <span class="badge">gemini-2.5-flash</span>
</div>
""", unsafe_allow_html=True)

# ── Message history ───────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">◈</div>
        <p>Start a conversation.<br>Ask anything — Gemini is listening.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        is_user = msg["role"] == "user"
        row_cls  = "user" if is_user else "ai"
        av_cls   = "user-av" if is_user else "ai-av"
        av_icon  = "👤" if is_user else "✦"
        sender   = "You" if is_user else "Gemini"

        st.markdown(f"""
        <div class="msg-row {row_cls}">
            <div class="avatar {av_cls}">{av_icon}</div>
            <div class="bubble">
                <div class="sender">{sender}</div>
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Message Gemini…")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build contents list for API
    contents = [
        m["role"] + ": " + m["content"]
        for m in st.session_state.messages
    ]

    # Call Gemini
    with st.spinner("Thinking…"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )
        ai_reply = response.text

    # Add AI message
    st.session_state.messages.append({"role": "AI", "content": ai_reply})

    st.rerun()