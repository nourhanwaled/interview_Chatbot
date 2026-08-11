"""Prompt templates for the interview assistant."""

from typing import Any


def build_system_message(
    name: str,
    experience: str,
    skills: str,
    level: str,
    position: str,
    company: str,
) -> str:
    """Build the HR interviewer system prompt from form values."""
    return (
        f"You are an HR executive that interviews an interviewee called {name} "
        f"with experience {experience} and skills {skills}. "
        f"You should interview them for the position {level} {position} "
        f"at the company {company}."
    )


def build_feedback_system_message() -> str:
    """Build the feedback tool system prompt (score + feedback format)."""
    return (
        "You are a helpful tool that provides feedback on an interviewee performance.\n"
        "Before the Feedback give a score of 1 to 10.\n"
        "Follow this format:\n"
        "Overall Score: //Your score\n"
        "Feedback: //Here you put your feedback\n"
        "Give only the feedback do not ask any additional questins."
    )


def build_conversation_history(messages: list[dict[str, Any]]) -> str:
    """Flatten chat messages into `role: content` lines for the feedback model."""
    return "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)


def build_feedback_user_message(messages: list[dict[str, Any]]) -> str:
    """Build the user message that sends the interview transcript for evaluation."""
    conversation_history = build_conversation_history(messages)
    return (
        "This is the interview you need to evaluate. "
        "Keep in mind that you are only a tool. "
        "And you should only answer using the format provided. "
        f"Interview:\n{conversation_history}"
    )


def build_feedback_messages(messages: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Build the feedback LLM messages (system format + interview transcript)."""
    return [
        {"role": "system", "content": build_feedback_system_message()},
        {"role": "user", "content": build_feedback_user_message(messages)},
    ]
