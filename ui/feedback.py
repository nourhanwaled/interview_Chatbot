"""FEEDBACK stage — review interview messages and show AI feedback."""

from openai import OpenAI
import streamlit as st

from config import FEEDBACK_MODEL
from prompts import build_feedback_messages
from services.openai_service import create_chat_completion


def render_feedback(client: OpenAI) -> None:
    """Show feedback when feedback_show is True, using shared messages."""
    if not st.session_state.feedback_show:
        st.warning("Feedback is not available yet.")
        return

    st.subheader("Interview Feedback", divider="rainbow")
    _ensure_feedback_generated(client)

    if st.session_state.feedback_text:
        st.markdown(st.session_state.feedback_text)
    else:
        st.info("Unable to generate feedback. Try again or restart the interview.")

    with st.expander("Interview transcript"):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            role = "You" if message["role"] == "user" else "Interviewer"
            st.markdown(f"**{role}:** {message['content']}")

    if st.button("Start over"):
        st.session_state.setup_complete = False
        st.session_state.chat_complete = False
        st.session_state.feedback_show = False
        st.session_state.user_message_count = 0
        st.session_state.messages = []
        st.session_state.feedback_text = ""
        st.rerun()


def _ensure_feedback_generated(client: OpenAI) -> None:
    if st.session_state.feedback_text:
        return

    with st.spinner("Generating feedback..."):
        feedback = create_chat_completion(
            client,
            build_feedback_messages(st.session_state.messages),
            model=FEEDBACK_MODEL,
        )
        if feedback:
            st.session_state.feedback_text = feedback
