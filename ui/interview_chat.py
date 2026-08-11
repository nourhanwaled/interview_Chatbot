"""INTERVIEW stage — chat until chat_complete is set."""

from openai import OpenAI
import streamlit as st

from config import MAX_USER_MESSAGES
from services.openai_service import stream_chat_reply


def render_interview_chat(client: OpenAI) -> None:
    """Render chat history, input, and streamed assistant replies."""
    st.info("Start by introducing yourself.")
    st.caption(
        f"Answers: {st.session_state.user_message_count} / {MAX_USER_MESSAGES}"
    )
    _render_message_history()
    _handle_user_input(client)


def _render_message_history() -> None:
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])


def _mark_chat_complete() -> None:
    """Move from INTERVIEW → FEEDBACK."""
    st.session_state.chat_complete = True
    st.session_state.feedback_show = True
    st.rerun()


def _handle_user_input(client: OpenAI) -> None:
    if st.session_state.chat_complete:
        return

    if st.button("End interview & get feedback"):
        _mark_chat_complete()
        return

    if not (prompt := st.chat_input("Your Answer.")):
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_message_count += 1
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = stream_chat_reply(client, st.session_state.messages)
        if response is None:
            # Drop the failed user turn so retry is clean
            st.session_state.messages.pop()
            st.session_state.user_message_count -= 1
            return

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

    if st.session_state.user_message_count >= MAX_USER_MESSAGES:
        _mark_chat_complete()
