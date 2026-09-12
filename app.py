"""Streamlit web interface for the SupportAI helpdesk agent."""

import logging
import os

import streamlit as st

from dotenv import load_dotenv
from task1 import faqs
from task2 import DEFAULT_MODEL, LLMClient
from task4 import SupportAgent

load_dotenv()
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="SupportAI Helpdesk",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #17221f;
        --muted: #71807a;
        --paper: #f5f7f2;
        --panel: #ffffff;
        --mint: #c9f2dd;
        --green: #166b4e;
        --line: #dfe7e1;
        --amber: #f4b860;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
        color-scheme: light;
    }

    [data-testid='stAppViewContainer'],
    [data-testid='stMain'],
    [data-testid='stSidebar'],
    [data-testid='stSidebar'] * {
        color: var(--ink) !important;
    }

    [data-testid='stSidebar'] {
        background: #eef3ed !important;
    }

    [data-testid='stSidebar'] [data-testid='stMarkdownContainer'] p,
    [data-testid='stSidebar'] [data-testid='stCaptionContainer'],
    [data-testid='stSidebar'] label {
        color: var(--muted) !important;
    }

    [data-testid='stChatMessage'],
    [data-testid='stChatMessage'] > div,
    [data-testid='stChatMessage'] [data-testid='stMarkdownContainer'],
    [data-testid='stChatMessage'] [data-testid='stMarkdownContainer'] p,
    [data-testid='stChatMessage'] [data-testid='stCaptionContainer'] {
        color: var(--ink) !important;
    }

    [data-testid='stChatMessage'] {
        background: #ffffff !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
    }

    [data-testid='stChatInput'] {
        background: #ffffff !important;
        border: 1px solid #b7c8bc !important;
        border-radius: 10px !important;
    }

    [data-testid='stChatInput'] > div,
    [data-testid='stChatInput'] form {
        background: #ffffff !important;
        border-radius: 10px !important;
    }

    [data-testid='stChatInput'] textarea,
    [data-testid='stChatInput'] textarea:focus {
        color: var(--ink) !important;
        background: #ffffff !important;
        -webkit-text-fill-color: var(--ink) !important;
    }

    [data-testid='stChatInput'] textarea::placeholder {
        color: var(--muted) !important;
        opacity: 1 !important;
    }

    [data-testid='stChatInput'] button {
        color: #ffffff !important;
        background: var(--green) !important;
        border-color: var(--green) !important;
    }

    [data-testid='stCaptionContainer'],
    [data-testid='stCaptionContainer'] * {
        color: var(--muted) !important;
    }

    .block-container { max-width: 1120px; padding-top: 0; padding-bottom: 1rem; }
    [data-testid='stHeader'] { background: transparent; }
    [data-testid='stToolbar'] { right: 1rem; }

    [data-testid='stSidebar'] { border-right: 1px solid var(--line); }

    div.stButton > button,
    div.stButton > button:hover,
    div.stButton > button:focus,
    div.stButton > button:active {
        color: var(--ink) !important;
        background: var(--panel) !important;
        border: 1px solid #b7c8bc !important;
        box-shadow: none !important;
    }

    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button div {
        color: inherit !important;
    }

    div.stButton > button:hover,
    div.stButton > button:focus-visible {
        color: var(--ink) !important;
        background: var(--mint) !important;
        border-color: var(--green) !important;
    }

    div.stButton > button[kind='primary'],
    div.stButton > button[kind='primary']:hover,
    div.stButton > button[kind='primary']:focus,
    div.stButton > button[kind='primary']:active {
        color: #ffffff !important;
        background: var(--green) !important;
        border-color: var(--green) !important;
    }

    div.stButton > button[kind='primary'] p,
    div.stButton > button[kind='primary'] span,
    div.stButton > button[kind='primary'] div {
        color: #ffffff !important;
    }

    h1, h2, h3, [data-testid='stMetricValue'] {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0;
    }

    .hero { padding: 0 0 5px; border-bottom: 1px solid var(--line); margin-bottom: 5px; }

    .eyebrow {
        color: var(--green);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3.6rem);
        line-height: 0.98;
        color: var(--ink);
    }

    .hero p {
        max-width: 510px;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.55;
        margin: 2px 0 0;
    }

    .hero-mark {
        display: inline-grid;
        place-items: center;
        width: 42px;
        height: 42px;
        margin-bottom: 4px;
        border-radius: 12px;
        background: var(--ink);
        color: var(--mint);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
    }

    .section-label {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 12px 0 8px;
    }

    .empty {
        padding: 54px 20px;
        border: 1px dashed #bdcbc0;
        border-radius: 8px;
        text-align: center;
        color: var(--muted);
    }

    .faq-item {
        padding: 11px 0;
        border-bottom: 1px solid var(--line);
    }
    .faq-item strong { display: block; font-size: 0.84rem; color: var(--ink); }
    .faq-item span { color: var(--muted); font-size: 0.74rem; }

    @media (max-width: 760px) {
        .block-container { padding: 0.5rem 0.85rem 1.25rem; }
        .hero h1 { font-size: 2.45rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_agent():
    """Create the session-scoped SupportAgent once."""
    if "agent" not in st.session_state:
        api_key = os.getenv("OPENROUTER_API_KEY")
        st.session_state.agent = SupportAgent(
            faqs,
            LLMClient(api_key=api_key, model=DEFAULT_MODEL) if api_key else None,
        )
    return st.session_state.agent


def render_turns(agent):
    """Render the conversation as question-and-answer pairs."""
    if not agent.conversation_history:
        st.markdown(
            "<div class='empty'><strong>Start with a question.</strong><br>"
            "Ask about passwords, orders, refunds, shipping, accounts, or subscriptions.</div>",
            unsafe_allow_html=True,
        )
        return

    turns = agent.conversation_history
    position = 0
    while position < len(turns):
        question = turns[position]
        if question.role == "user":
            with st.chat_message("user"):
                st.write(question.content)

            position += 1
            if position < len(turns) and turns[position].role == "assistant":
                answer = turns[position]
                with st.chat_message("assistant"):
                    st.write(answer.content)
                    metadata = []
                    if answer.faq_id:
                        metadata.append(f"FAQ: {answer.faq_id}")
                    if answer.confidence is not None:
                        metadata.append(f"Confidence: {answer.confidence:.2f}")
                    if metadata:
                        st.caption(" · ".join(metadata))
        else:
            with st.chat_message("assistant"):
                st.write(question.content)
                if question.confidence is not None:
                    st.caption(f"Confidence: {question.confidence:.2f}")
        position += 1


def submit_message(agent, prompt):
    """Send a submitted prompt; SupportAgent preserves match metadata on errors."""
    if agent.llm_client is None:
        st.session_state["configuration_error"] = True

    agent.handle_message(prompt)


agent = get_agent()

with st.sidebar:
    st.markdown("## SupportAI")
    st.caption("Grounded customer support")
    if st.button("New conversation", use_container_width=True, type="primary"):
        agent.reset()
        st.rerun()
    if st.button("Escalate to human support", use_container_width=True):
        agent.escalate()
        st.rerun()

    st.markdown("<div class='section-label'>Try asking</div>", unsafe_allow_html=True)
    for suggestion in [
        "I forgot my login credentials",
        "Where is my package?",
        "Can I get a refund?",
    ]:
        if st.button(suggestion, key=f"suggestion_{suggestion}", use_container_width=True):
            submit_message(agent, suggestion)
            st.rerun()

    st.markdown("<div class='section-label'>FAQ index</div>", unsafe_allow_html=True)
    faq_filter = st.text_input(
        "Search FAQs",
        placeholder="Search by topic or keyword",
        label_visibility="collapsed",
    ).strip().lower()
    visible_faqs = [
        faq for faq in faqs
        if not faq_filter
        or faq_filter in faq["question"].lower()
        or faq_filter in faq["category"].lower()
        or any(faq_filter in keyword.lower() for keyword in faq["keywords"])
    ]
    if not visible_faqs:
        st.caption("No FAQs match that search.")
    for faq in visible_faqs:
        st.markdown(
            f"<div class='faq-item'><strong>{faq['question']}</strong><span>{faq['category']} · {faq['id']}</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-label'>Connection</div>", unsafe_allow_html=True)
    if agent.llm_client:
        st.success("OpenRouter connected")
    else:
        st.warning("Add OPENROUTER_API_KEY to .env")

st.markdown(
    "<div class='hero'><div><div class='eyebrow'>SupportAI · Helpdesk</div>"
    "<h1>How can we help?</h1><p>Ask about your account, order, billing, or subscription.</p></div></div>",
    unsafe_allow_html=True,
)

if st.session_state.pop("configuration_error", False):
    st.error("Add a valid OPENROUTER_API_KEY to your .env file before sending questions.")

st.markdown("<div class='section-label'>Conversation</div>", unsafe_allow_html=True)
render_turns(agent)
prompt = st.chat_input("Ask SupportAI a question...")
if prompt:
    submit_message(agent, prompt.strip())
    st.rerun()
st.caption("Press Enter to send · Answers stay grounded in the verified FAQ index")
