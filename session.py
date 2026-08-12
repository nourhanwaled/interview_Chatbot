"""Session state helpers."""

# --- Imports ---
import streamlit as st

from config import SESSION_DEFAULTS


def init_session_state() -> None:
    """Ensure all expected session keys exist with defaults (run once per key)."""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
