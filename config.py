"""App-wide constants and defaults."""

PAGE_TITLE = "Streamlit Chatbot"
PAGE_ICON = "🤖"

OPENAI_MODEL = "gpt-4o-mini"
FEEDBACK_MODEL = "gpt-4o"

# Interview ends after this many user replies, then feedback is shown
MAX_USER_MESSAGES = 5

LEVEL_OPTIONS = ["Junior", "Mid Level", "Senior Level"]
POSITION_OPTIONS = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
]
COMPANY_OPTIONS = ["Google", "Apple", "Microsoft", "Amazon", "Facebook"]

REQUIRED_FIELDS = ("name", "experience", "skills", "level", "position", "company")

SESSION_DEFAULTS = {
    # --- Profile (SET UP) ---
    "name": "",
    "experience": "",
    "skills": "",
    "level": LEVEL_OPTIONS[0],
    "position": POSITION_OPTIONS[0],
    "company": COMPANY_OPTIONS[0],
    # --- Stage flags (see diagram: SET UP → INTERVIEW → FEEDBACK) ---
    "setup_complete": False,
    "user_message_count": 0,
    "chat_complete": False,
    "feedback_show": False,
    # --- Shared chat ---
    "messages": [],
    "feedback_text": "",
    "openai_model": OPENAI_MODEL,
}
