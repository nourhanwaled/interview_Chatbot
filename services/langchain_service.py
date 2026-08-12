"""LangChain LLM service: Groq (default) or OpenAI, streaming + feedback LCEL."""

from __future__ import annotations

# --- Imports ---
from typing import Any, Iterator

import streamlit as st
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from openai import RateLimitError

from config import (
    LLM_PROVIDER,
    feedback_model_name,
    interview_model_name,
)
from prompts import dict_messages_to_langchain, get_feedback_prompt


# --- Secrets / model factory ---
def _get_secret(name: str) -> str:
    """Read a required key from Streamlit secrets."""
    try:
        return st.secrets[name]
    except Exception as exc:
        raise RuntimeError(
            f'Missing secret "{name}" in .streamlit/secrets.toml for provider "{LLM_PROVIDER}".'
        ) from exc


def get_chat_model(model: str | None = None, *, streaming: bool = False) -> BaseChatModel:
    """
    Create the chat model for the active provider.

    - groq   → ChatGroq (free tier, no OpenAI credits)
    - openai → ChatOpenAI (needs billing)

    Always uses the provider's configured model names so a stale session
    value like "gpt-4o-mini" cannot force OpenAI while provider is groq.
    """
    model_name = model or interview_model_name()
    # Keep session in sync for UI display
    st.session_state["llm_model"] = model_name

    if LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=model_name,
            api_key=_get_secret("OPEN_API_KEY"),
            streaming=streaming,
        )

    if LLM_PROVIDER == "groq":
        api_key = _get_secret("GROQ_API_KEY")
        if not str(api_key).strip():
            raise RuntimeError(
                'GROQ_API_KEY is empty. Add your free key from '
                "https://console.groq.com/keys to .streamlit/secrets.toml"
            )
        return ChatGroq(
            model=model_name,
            api_key=api_key,
            streaming=streaming,
        )

    raise ValueError(
        f'Unsupported LLM_PROVIDER="{LLM_PROVIDER}". Use "groq" or "openai" in config.py.'
    )


# --- Error handling (billing / rate limits) ---
def _error_text(error: BaseException) -> str:
    return str(error).lower()


def is_no_balance_error(error: BaseException) -> bool:
    """Detect insufficient-quota / no-credits style errors (mostly OpenAI)."""
    body = getattr(error, "body", None)
    error_code = None
    if isinstance(body, dict):
        error_code = (body.get("error") or {}).get("code")

    message = _error_text(error)
    return error_code in ("insufficient_quota", "credit_balance_exhausted") or (
        "no credits remaining" in message
        or "credit_balance_exhausted" in message
        or "insufficient_quota" in message
    )


def is_rate_limit_error(error: BaseException) -> bool:
    """True for provider rate-limit / quota errors we can show nicely."""
    if isinstance(error, RateLimitError):
        return True
    message = _error_text(error)
    return any(
        token in message
        for token in (
            "rate limit",
            "rate_limit",
            "too many requests",
            "quota",
            "429",
        )
    )


def show_llm_error(error: BaseException) -> None:
    """Render a user-friendly message for LLM failures."""
    if is_no_balance_error(error):
        st.error(
            "No balance: your OpenAI account has no credits remaining. "
            "Add credits, or set LLM_PROVIDER = \"groq\" in config.py and use a GROQ_API_KEY."
        )
        return

    if is_rate_limit_error(error):
        st.error("Rate limit reached. Please wait a moment and try again.")
        return

    st.error(f"LLM error: {error}")


# --- INTERVIEW: stream tokens into Streamlit ---
def _token_stream(messages: list[dict[str, Any]]) -> Iterator[str]:
    """Yield text chunks from the interview LLM (used by st.write_stream)."""
    llm = get_chat_model(streaming=True)
    for chunk in llm.stream(dict_messages_to_langchain(messages)):
        if chunk.content:
            yield str(chunk.content)


def stream_chat_reply(messages: list[dict[str, Any]]) -> str | None:
    """
    Stream an interview reply into the Streamlit UI via LangChain.

    Returns the full response text on success, or None on handled LLM errors.
    """
    try:
        return st.write_stream(_token_stream(messages))
    except Exception as error:
        if is_rate_limit_error(error) or is_no_balance_error(error):
            show_llm_error(error)
            return None
        raise


# --- FEEDBACK: LCEL chain (prompt | model | parser) ---
def generate_feedback(messages: list[dict[str, Any]]) -> str | None:
    """
    Run the feedback LCEL chain: prompt | model | string parser.

    Returns feedback text on success, or None on handled LLM errors.
    """
    conversation_history = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in messages
    )

    # LCEL: ChatPromptTemplate → ChatGroq/ChatOpenAI → plain string
    chain = (
        get_feedback_prompt()
        | get_chat_model(feedback_model_name())
        | StrOutputParser()
    )

    try:
        return chain.invoke({"conversation_history": conversation_history})
    except Exception as error:
        if is_rate_limit_error(error) or is_no_balance_error(error):
            show_llm_error(error)
            return None
        raise
