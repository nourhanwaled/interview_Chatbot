"""Form validation helpers."""

# --- Imports ---
import streamlit as st

from config import REQUIRED_FIELDS


def all_fields_filled() -> bool:
    """Return True when every required interview field has a non-empty value."""
    return all(
        str(st.session_state.get(field, "")).strip() for field in REQUIRED_FIELDS
    )
