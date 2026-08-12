"""App-wide constants and defaults."""

# --- Page ---
PAGE_TITLE = "Streamlit Chatbot"
PAGE_ICON = "🤖"

# --- LLM provider ---
# "groq"  = free-tier cloud (recommended when OpenAI has no credits)
# "openai" = needs OpenAI billing / credits
LLM_PROVIDER = "groq"

# --- Groq models (https://console.groq.com) ---
GROQ_INTERVIEW_MODEL = "llama-3.1-8b-instant"
GROQ_FEEDBACK_MODEL = "llama-3.3-70b-versatile"

# --- OpenAI models (only used when LLM_PROVIDER = "openai") ---
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_FEEDBACK_MODEL = "gpt-4o"

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


def interview_model_name() -> str:
    """Model id for the INTERVIEW stage based on provider."""
    if LLM_PROVIDER == "openai":
        return OPENAI_MODEL
    return GROQ_INTERVIEW_MODEL


def feedback_model_name() -> str:
    """Model id for the FEEDBACK stage based on provider."""
    if LLM_PROVIDER == "openai":
        return OPENAI_FEEDBACK_MODEL
    return GROQ_FEEDBACK_MODEL


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
    "llm_model": interview_model_name(),
}
