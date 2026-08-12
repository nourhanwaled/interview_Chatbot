"""LangChain prompts and LCEL message builders."""

# --- Imports ---
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


# --- INTERVIEW system prompt (built from setup form) ---
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


# --- FEEDBACK system prompt (score 1–10 + feedback format) ---
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


# --- Transcript helpers ---
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


# --- Convert session messages → LangChain message objects ---
def dict_messages_to_langchain(messages: list[dict[str, Any]]) -> list[BaseMessage]:
    """Convert session `messages` dicts into LangChain message objects."""
    converted: list[BaseMessage] = []
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            converted.append(SystemMessage(content=content))
        elif role == "user":
            converted.append(HumanMessage(content=content))
        elif role == "assistant":
            converted.append(AIMessage(content=content))
    return converted


# --- FEEDBACK ChatPromptTemplate (used in LCEL chain) ---
def get_feedback_prompt() -> ChatPromptTemplate:
    """LCEL prompt for the FEEDBACK stage."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", build_feedback_system_message()),
            (
                "human",
                "This is the interview you need to evaluate. "
                "Keep in mind that you are only a tool. "
                "And you should only answer using the format provided. "
                "Interview:\n{conversation_history}",
            ),
        ]
    )
