"""OpenAI client and chat helpers."""

from __future__ import annotations

from typing import Any

import streamlit as st
from openai import OpenAI, RateLimitError


def get_client() -> OpenAI:
    """Create an OpenAI client using the Streamlit secret key."""
    return OpenAI(api_key=st.secrets["OPEN_API_KEY"])


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


def stream_chat_reply(client: OpenAI, messages: list[dict[str, Any]]) -> str | None:
    """
    Stream an assistant reply into the UI.

    Returns the response text on success, or None if a rate-limit error occurred.
    """
    try:
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        return st.write_stream(stream)
    except RateLimitError as error:
        show_rate_limit_error(error)
        return None


def create_chat_completion(
    client: OpenAI,
    messages: list[dict[str, Any]],
    *,
    model: str | None = None,
) -> str | None:
    """
    Non-streaming completion (used for feedback).

    Returns the response text on success, or None if a rate-limit error occurred.
    """
    try:
        response = client.chat.completions.create(
            model=model or st.session_state["openai_model"],
            messages=messages,
        )
        return response.choices[0].message.content
    except RateLimitError as error:
        show_rate_limit_error(error)
        return None
