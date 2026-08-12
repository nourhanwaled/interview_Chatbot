"""App-wide constants and defaults."""

# --- Page ---
PAGE_TITLE = "Streamlit Chatbot"
PAGE_ICON = "🤖"

# --- Models ---
OPENAI_MODEL = "gpt-4o-mini"  # interview chat
FEEDBACK_MODEL = "gpt-4o"  # final scoring / feedback

# --- Interview length ---
# Ends after this many user replies, then feedback is shown
MAX_USER_MESSAGES = 5

# --- Form options ---
LEVEL_OPTIONS = ["Junior", "Mid Level", "Senior Level"]
POSITION_OPTIONS = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
]
COMPANY_OPTIONS = ["Google", "Apple", "Microsoft", "Amazon", "Facebook"]

# Fields that must be non-empty before Start Interview
REQUIRED_FIELDS = ("name", "experience", "skills", "level", "position", "company")

# --- Session state defaults (SET UP → INTERVIEW → FEEDBACK) ---
SESSION_DEFAULTS = {
    # Profile (SET UP)
    "name": "",
    "experience": "",
    "skills": "",
    "level": LEVEL_OPTIONS[0],
    "position": POSITION_OPTIONS[0],
    "company": COMPANY_OPTIONS[0],
    # Stage flags
    "setup_complete": False,
    "user_message_count": 0,
    "chat_complete": False,
    "feedback_show": False,
    # Shared chat + feedback cache
    "messages": [],
    "feedback_text": "",
    "openai_model": OPENAI_MODEL,
}
