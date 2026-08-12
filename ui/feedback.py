"""FEEDBACK stage — review interview messages and show AI feedback."""

# --- Imports ---
import streamlit as st

from services.langchain_service import generate_feedback


def render_feedback() -> None:
    """Show feedback when feedback_show is True, using shared messages."""
    if not st.session_state.feedback_show:
        st.warning("Feedback is not available yet.")
        return

    # --- Generate + display score/feedback ---
    st.subheader("Interview Feedback", divider="rainbow")
    _ensure_feedback_generated()

    if st.session_state.feedback_text:
        st.markdown(st.session_state.feedback_text)
    else:
        st.info("Unable to generate feedback. Try again or restart the interview.")

    # --- Optional transcript review ---
    with st.expander("Interview transcript"):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            role = "You" if message["role"] == "user" else "Interviewer"
            st.markdown(f"**{role}:** {message['content']}")

    # --- Reset all stage flags and go back to SET UP ---
    if st.button("Start over"):
        st.session_state.setup_complete = False
        st.session_state.chat_complete = False
        st.session_state.feedback_show = False
        st.session_state.user_message_count = 0
        st.session_state.messages = []
        st.session_state.feedback_text = ""
        st.rerun()


def _ensure_feedback_generated() -> None:
    """Call LangChain feedback chain once; cache result in session state."""
    if st.session_state.feedback_text:
        return

    with st.spinner("Generating feedback..."):
        feedback = generate_feedback(st.session_state.messages)
        if feedback:
            st.session_state.feedback_text = feedback
