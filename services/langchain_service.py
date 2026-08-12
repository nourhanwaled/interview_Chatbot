"""LangChain / OpenAI service: LLMs, streaming interview, feedback chain."""

from __future__ import annotations

# --- Imports ---
from typing import Any, Iterator

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import RateLimitError

from config import FEEDBACK_MODEL, OPENAI_MODEL
from prompts import dict_messages_to_langchain, get_feedback_prompt


# --- Model helpers ---
def get_api_key() -> str:
    """Read the OpenAI API key from Streamlit secrets."""
    return st.secrets["OPEN_API_KEY"]


def get_chat_model(model: str | None = None, *, streaming: bool = False) -> ChatOpenAI:
    """Create a LangChain ChatOpenAI model (interview or feedback)."""
    return ChatOpenAI(
        model=model or st.session_state.get("openai_model", OPENAI_MODEL),
        api_key=get_api_key(),
        streaming=streaming,
    )


# --- Error handling (billing / rate limits) ---
def is_no_balance_error(error: RateLimitError) -> bool:
    """Detect insufficient-quota / no-credits rate limit errors."""
    body = error.body if isinstance(getattr(error, "body", None), dict) else {}
    error_code = (body.get("error") or {}).get("code")
    message = str(error).lower()

    return error_code in ("insufficient_quota", "credit_balance_exhausted") or (
        "no credits remaining" in message or "credit_balance_exhausted" in message
    )


def show_rate_limit_error(error: RateLimitError) -> None:
    """Render a user-friendly message for rate-limit / billing errors."""
    if is_no_balance_error(error):
        st.error(
            "No balance: your OpenAI account has no credits remaining. "
            "Add credits at https://platform.openai.com/settings/organization/billing/"
        )
    else:
        st.error("Rate limit reached. Please wait a moment and try again.")


# --- INTERVIEW: stream tokens into Streamlit ---
def _token_stream(messages: list[dict[str, Any]]) -> Iterator[str]:
    """Yield text chunks from the interview LLM (used by st.write_stream)."""
    llm = get_chat_model(streaming=True)
    # Convert session dicts → LangChain messages, then stream
    for chunk in llm.stream(dict_messages_to_langchain(messages)):
        if chunk.content:
            yield str(chunk.content)


def stream_chat_reply(messages: list[dict[str, Any]]) -> str | None:
    """
    Stream an interview reply into the Streamlit UI via LangChain.

    Returns the full response text on success, or None on rate-limit errors.
    """
    try:
        return st.write_stream(_token_stream(messages))
    except RateLimitError as error:
        show_rate_limit_error(error)
        return None


# --- FEEDBACK: LCEL chain (prompt | model | parser) ---
def generate_feedback(messages: list[dict[str, Any]]) -> str | None:
    """
    Run the feedback LCEL chain: prompt | model | string parser.

    Returns feedback text on success, or None on rate-limit errors.
    """
    # Flatten chat history for the feedback prompt variable
    conversation_history = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in messages
    )

    # LCEL: ChatPromptTemplate → ChatOpenAI(gpt-4o) → plain string
    chain = get_feedback_prompt() | get_chat_model(FEEDBACK_MODEL) | StrOutputParser()

    try:
        return chain.invoke({"conversation_history": conversation_history})
    except RateLimitError as error:
        show_rate_limit_error(error)
        return None
