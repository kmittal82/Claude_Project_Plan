"""
EquityIQ — Equity Compensation Assistant
Grok-style: Logo → Search bar → Sample pills | CEP Level 1 | Powered by Claude
"""

import os

import streamlit as st
from anthropic import Anthropic, APIConnectionError, APIError, RateLimitError
from dotenv import load_dotenv

from system_prompt import SYSTEM_PROMPT

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EquityIQ",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Constants ──────────────────────────────────────────────────────────────────
MODEL      = os.getenv("CLAUDE_MODEL", "claude-opus-4-6")
MAX_TOKENS = 1500
API_KEY    = os.getenv("ANTHROPIC_API_KEY")

# Most-asked questions — shown as cards on the landing page
QUESTIONS = [
    "What's the tax difference between ISOs and NSOs?",
    "When should I file an 83(b) election and what's the deadline?",
    "How does the ESPP lookback provision save me money?",
    "What taxes are withheld when my RSUs vest?",
]


# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0D0D0D !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"]        { display: none !important; }
    .block-container {
        max-width: 720px !important;
        padding: 0 1.5rem 3rem !important;
        margin: 0 auto !important;
    }

    /* ── Landing: full-page centering ── */
    .eq-landing {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 12vh;
        text-align: center;
    }

    /* ── Logo / wordmark ── */
    .eq-wordmark {
        font-size: 3rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -2px;
        line-height: 1;
        margin-bottom: 2rem;
    }
    .eq-wordmark span { color: #7C6FD4; }

    /* ── Search bar (text_input styled as Grok-style bar) ── */
    div[data-testid="stTextInput"] {
        width: 100%;
    }
    div[data-testid="stTextInput"] > label { display: none !important; }

    /* The visual search bar lives on the ROOT element (not the raw input).
       This way the border/radius never gets clipped by any parent overflow. */
    div[data-testid="stTextInputRootElement"] {
        overflow: hidden !important;        /* clips input text to rounded shape  */
        border: 1.5px solid #3A3A3A !important;
        border-radius: 50px !important;
        background: #161616 !important;
        margin: 0 4px !important;           /* breathing room — prevents edge cut  */
        padding: 0 !important;
        height: 60px !important;            /* match input height so padding is equal top/bottom */
        box-shadow: none !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div[data-testid="stTextInputRootElement"]:focus-within {
        border-color: #5A52A0 !important;
        box-shadow: 0 0 0 4px rgba(124,111,212,0.12) !important;
    }

    /* Input itself is transparent inside the styled container */
    div[data-testid="stTextInput"] input {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.95rem 1.8rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        color: #E0E0E0 !important;
        height: 60px !important;
        caret-color: #7C6FD4 !important;
        width: 100% !important;
        box-sizing: border-box !important;
        outline: none !important;
        box-shadow: none !important;
        text-align: left !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #555 !important;
        text-align: left !important;
    }

    /* ── Question cards (most-asked questions) ── */
    div[data-testid="stColumn"] .stButton > button {
        background: #111 !important;
        border: 1px solid #242424 !important;
        border-radius: 14px !important;
        color: #909090 !important;
        font-size: 0.83rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        padding: 0.85rem 1.1rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        text-align: left !important;
        line-height: 1.45 !important;
        transition: border-color 0.15s, color 0.15s, background 0.15s !important;
        cursor: pointer !important;
        width: 100% !important;
        height: auto !important;
        min-height: 70px !important;
    }
    div[data-testid="stColumn"] .stButton > button:hover {
        border-color: #3A3A3A !important;
        color: #D0D0D0 !important;
        background: #161616 !important;
    }

    /* ── Chat mode header ── */
    .eq-chat-header {
        padding: 1rem 0 0.8rem;
        border-bottom: 1px solid #1C1C1C;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .eq-chat-logo {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFF;
        letter-spacing: -0.5px;
    }
    .eq-chat-logo span { color: #7C6FD4; }
    .eq-chat-badge {
        display: inline-block;
        font-size: 0.68rem;
        color: #444;
        background: #111;
        border: 1px solid #222;
        border-radius: 6px;
        padding: 0.12rem 0.5rem;
        margin-left: 0.5rem;
        vertical-align: middle;
        font-weight: 500;
    }

    /* ── Clear button ── */
    .eq-clear-wrap .stButton > button {
        background: transparent !important;
        border: 1px solid #252525 !important;
        color: #555 !important;
        border-radius: 8px !important;
        padding: 0.28rem 0.75rem !important;
        font-size: 0.75rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.15s !important;
    }
    .eq-clear-wrap .stButton > button:hover {
        border-color: #3A3A3A !important;
        color: #AAA !important;
        background: #181818 !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.2rem 0 !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #0F1120 !important;
        border: 1px solid #191E38 !important;
        border-radius: 16px !important;
        padding: 0.8rem 1rem !important;
        margin: 0.3rem 0 !important;
    }
    [data-testid="stChatMessage"] p {
        color: #D0D0D0;
        line-height: 1.75;
        font-size: 0.93rem;
    }
    [data-testid="stChatMessage"] strong { color: #FFF; }
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3 {
        color: #EAEAEA;
        font-weight: 600;
        margin-top: 1rem;
        font-size: 1rem;
    }
    [data-testid="stChatMessage"] li { color: #C0C0C0; font-size: 0.91rem; line-height: 1.7; }
    [data-testid="stChatMessage"] code {
        background: #181826; color: #A8B4FF;
        padding: 0.15em 0.4em; border-radius: 4px; font-size: 0.84em;
    }
    [data-testid="stChatMessage"] table { width: 100%; border-collapse: collapse; margin: 0.8rem 0; }
    [data-testid="stChatMessage"] th {
        background: #181824; color: #8888CC; padding: 0.45rem 0.75rem;
        text-align: left; font-size: 0.74rem; text-transform: uppercase;
        letter-spacing: 0.06em; border-bottom: 1px solid #222;
    }
    [data-testid="stChatMessage"] td {
        padding: 0.4rem 0.75rem; border-bottom: 1px solid #1A1A1A; color: #B8B8B8;
    }

    /* ── Avatars ── */
    [data-testid="chatAvatarIcon-assistant"] {
        background: #12122A !important; border: 1px solid #25254A !important;
        color: #7C6FD4 !important; font-size: 0.8rem !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background: #1A1A1A !important; border: 1px solid #2A2A2A !important;
    }

    /* ── Chat input (chat mode) ── */
    [data-testid="stChatInputContainer"] {
        background: #111 !important;
        border: 1.5px solid #272727 !important;
        border-radius: 50px !important;
        padding: 0.15rem 0.5rem !important;
        box-shadow: 0 2px 24px rgba(0,0,0,0.5) !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stChatInputContainer"]:focus-within {
        border-color: #3D3870 !important;
        box-shadow: 0 2px 24px rgba(0,0,0,0.5), 0 0 0 4px rgba(124,111,212,0.08) !important;
    }
    [data-testid="stChatInputContainer"] textarea {
        background: transparent !important; color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif !important; font-size: 0.93rem !important;
        caret-color: #7C6FD4 !important;
    }
    [data-testid="stChatInputContainer"] textarea::placeholder { color: #444 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #272727; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #383838; }
    </style>
    """, unsafe_allow_html=True)


# ── Anthropic client ───────────────────────────────────────────────────────────
@st.cache_resource
def get_anthropic_client():
    if not API_KEY:
        return None
    return Anthropic(api_key=API_KEY)

client = get_anthropic_client()


# ── Session state ──────────────────────────────────────────────────────────────
def init_session_state():
    for k, v in {"messages": [], "pending_input": None}.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()


# ── API streaming ──────────────────────────────────────────────────────────────
def stream_response(history: list) -> str | None:
    try:
        with client.messages.stream(
            model=MODEL, max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT, messages=history, temperature=0.3,
        ) as stream:
            return st.write_stream(stream.text_stream)
    except RateLimitError:
        st.error("Rate limit reached — please wait a moment.")
    except APIConnectionError:
        st.error("Connection error. Check your internet and retry.")
    except APIError as e:
        st.error(f"API error ({e.status_code}): {e.message}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None


# ── Chat handler ───────────────────────────────────────────────────────────────
def handle_user_input(user_input: str):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response = stream_response(st.session_state.messages)

    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.session_state.messages.pop()


# ── LANDING PAGE ───────────────────────────────────────────────────────────────
def render_landing():
    # ── Logo ──
    st.markdown(
        '<div class="eq-wordmark" style="text-align:center;padding-top:12vh;margin-bottom:2rem;">'
        'Equity<span>IQ</span></div>',
        unsafe_allow_html=True,
    )

    # ── Search bar (text_input — submits on Enter) ──
    query = st.text_input(
        label="search",
        placeholder="Ask about equity compensation…",
        label_visibility="collapsed",
        key="landing_query",
    )
    if query and query.strip():
        st.session_state.pending_input = query.strip()
        st.rerun()

    # ── Most-asked question cards (2 × 2 grid) ──
    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
    row1, row2 = st.columns(2), st.columns(2)
    for i, question in enumerate(QUESTIONS):
        col = row1[i] if i < 2 else row2[i - 2]
        with col:
            if st.button(question, key=f"q_{i}", use_container_width=True):
                st.session_state.pending_input = question
                st.rerun()


# ── CHAT PAGE ──────────────────────────────────────────────────────────────────
def render_chat():
    # Header bar
    h1, h2 = st.columns([6, 1])
    with h1:
        st.markdown(
            '<div class="eq-chat-header">'
            '<div class="eq-chat-logo">Equity<span>IQ</span>'
            '<span class="eq-chat-badge">CEP L1</span></div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with h2:
        st.markdown(
            '<div class="eq-clear-wrap" style="padding-top:1rem">',
            unsafe_allow_html=True,
        )
        if st.button("Clear", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Existing conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Process pending prompt (from pill click or first typed message)
    if st.session_state.pending_input:
        pending = st.session_state.pending_input
        st.session_state.pending_input = None
        handle_user_input(pending)

    # Persistent chat input (Streamlit pins this to the bottom)
    user_input = st.chat_input("Ask a follow-up question…")
    if user_input and user_input.strip():
        handle_user_input(user_input.strip())


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()

    if client is None:
        st.error("**ANTHROPIC_API_KEY not set.** Add it to `equity-admin-bot/.env` and restart.")
        st.stop()

    in_chat = bool(st.session_state.messages) or bool(st.session_state.pending_input)

    if in_chat:
        render_chat()
    else:
        render_landing()


if __name__ == "__main__":
    main()
