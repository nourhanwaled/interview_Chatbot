"""
Interview chatbot entry point.

Stages (session flags):
  SET UP     → setup_complete
  INTERVIEW  → user_message_count, chat_complete, messages
  FEEDBACK   → feedback_show, messages

LLM calls go through LangChain (see services/langchain_service.py).
"""

import streamlit as st

from config import (
    LLM_PROVIDER,
    PAGE_ICON,
    PAGE_TITLE,
    feedback_model_name,
    interview_model_name,
)
from session import init_session_state
from ui.feedback import render_feedback
from ui.interview_chat import render_interview_chat
from ui.setup_form import render_setup_form

# --- Page setup ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(PAGE_TITLE)

# --- Session ---
init_session_state()
# Force provider models (clears stale OpenAI model names from old sessions)
st.session_state["llm_model"] = interview_model_name()

# --- Show which free/paid backend is active ---
st.caption(
    f"Provider: **{LLM_PROVIDER}** · "
    f"Interview: `{interview_model_name()}` · "
    f"Feedback: `{feedback_model_name()}`"
)

if LLM_PROVIDER == "groq":
    groq_key = str(st.secrets.get("GROQ_API_KEY", "")).strip()
    if not groq_key:
        st.error(
            "GROQ_API_KEY is missing or empty in `.streamlit/secrets.toml`. "
            "Get a free key at https://console.groq.com/keys and restart the app."
        )
        st.stop()

# --- Stage routing: SET UP → INTERVIEW → FEEDBACK ---
if not st.session_state.setup_complete:
    render_setup_form()
elif not st.session_state.chat_complete:
    render_interview_chat()
else:
    render_feedback()
