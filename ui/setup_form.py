"""SET UP stage — collect candidate details before the interview."""

# --- Imports ---
import streamlit as st

from config import COMPANY_OPTIONS, LEVEL_OPTIONS, POSITION_OPTIONS
from prompts import build_system_message
from validation import all_fields_filled


def render_setup_form() -> None:
    """Render personal info + company/position form and start-interview action."""
    _render_personal_information()
    _render_company_and_position()
    _render_start_button()


# --- Personal information fields ---
def _render_personal_information() -> None:
    st.subheader("Personal Information", divider="rainbow")

    st.text_input(
        label="Name", max_chars=None, placeholder="Enter your name", key="name"
    )
    st.text_area(
        label="Experience",
        max_chars=None,
        placeholder="Enter your experience",
        key="experience",
    )
    st.text_area(
        label="Skills",
        max_chars=None,
        placeholder="Enter your skills",
        key="skills",
    )

    # Live summary of what the user typed
    st.write(f"**Your Name:** {st.session_state.name}")
    st.write(f"**Your Experience:** {st.session_state.experience}")
    st.write(f"**Your Skills:** {st.session_state.skills}")


# --- Level / position / company selectors ---
def _render_company_and_position() -> None:
    st.subheader("Company and Position", divider="rainbow")

    col1, col2 = st.columns(2)
    with col1:
        st.radio(label="Choose level", key="level", options=LEVEL_OPTIONS)

    with col2:
        st.selectbox(
            label="Choose position",
            key="position",
            options=POSITION_OPTIONS,
        )

    st.selectbox(
        label="Choose company",
        key="company",
        options=COMPANY_OPTIONS,
    )

    st.write(
        f"**Your information:** {st.session_state.level} "
        f"{st.session_state.position} at {st.session_state.company}"
    )


# --- Start Interview (validate → init chat → enter INTERVIEW stage) ---
def _render_start_button() -> None:
    if st.button("Start Interview", type="primary"):
        if not all_fields_filled():
            st.error(
                "Please fill in all fields (Name, Experience, and Skills) "
                "before starting the interview."
            )
            return

        # Seed chat with the HR system prompt
        st.session_state.messages = [
            {
                "role": "system",
                "content": build_system_message(
                    name=st.session_state.name,
                    experience=st.session_state.experience,
                    skills=st.session_state.skills,
                    level=st.session_state.level,
                    position=st.session_state.position,
                    company=st.session_state.company,
                ),
            }
        ]
        # Reset interview / feedback flags for a fresh run
        st.session_state.user_message_count = 0
        st.session_state.chat_complete = False
        st.session_state.feedback_show = False
        st.session_state.feedback_text = ""
        st.session_state.setup_complete = True
        st.rerun()
