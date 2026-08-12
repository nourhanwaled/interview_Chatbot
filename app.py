"""
Interview chatbot entry point.

Stages (session flags):
  SET UP     → setup_complete
  INTERVIEW  → user_message_count, chat_complete, messages
  FEEDBACK   → feedback_show, messages

LLM calls go through LangChain (see services/langchain_service.py).
"""

import streamlit as st

from config import PAGE_ICON, PAGE_TITLE
from session import init_session_state
from ui.feedback import render_feedback
from ui.interview_chat import render_interview_chat
from ui.setup_form import render_setup_form

# --- Page setup ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(PAGE_TITLE)

# --- Session ---
init_session_state()

# --- Stage routing: SET UP → INTERVIEW → FEEDBACK ---
if not st.session_state.setup_complete:
    render_setup_form()
elif not st.session_state.chat_complete:
    render_interview_chat()
else:
    render_feedback()
