# Chat Interview Project

Streamlit app that runs a mock HR interview with OpenAI across three stages: **SET UP → INTERVIEW → FEEDBACK**.

---

## Quick start

1. Install dependencies:

```bash
pip install streamlit openai
```

2. Add your OpenAI API key in `.streamlit/secrets.toml`:

```toml
OPEN_API_KEY = "sk-..."
```

3. Run the app:

```bash
streamlit run app.py
```

---

## How the app works

```
SET UP  →  INTERVIEW  →  FEEDBACK
```

1. **SET UP** — user enters name, experience, skills, level, position, and company. Sets `setup_complete`.
2. **INTERVIEW** — chat with the AI interviewer. Tracks `user_message_count` and `messages`. When the limit is reached (or user ends early), sets `chat_complete`.
3. **FEEDBACK** — when `feedback_show` is true, generates feedback from the shared `messages` transcript.

---

## Project structure

```
chat_interview_project/
├── app.py                      # Entry point: routes SET UP → INTERVIEW → FEEDBACK
├── config.py                   # Constants, option lists, session defaults
├── session.py                  # Initialize Streamlit session state
├── prompts.py                  # Interview system prompt + feedback prompt
├── validation.py               # Form field validation helpers
├── services/
│   ├── __init__.py
│   └── openai_service.py       # OpenAI client, streaming, completions, errors
├── ui/
│   ├── __init__.py
│   ├── setup_form.py           # SET UP stage UI
│   ├── interview_chat.py       # INTERVIEW stage UI
│   └── feedback.py             # FEEDBACK stage UI
├── .streamlit/
│   └── secrets.toml            # Local secrets (API key) — do not commit real keys
└── README.md                   # This file — keep in sync with the project
```

### Module responsibilities

| File / folder | Responsibility |
|---|---|
| `app.py` | Thin entry point. Routes by stage flags. |
| `config.py` | App-wide constants: titles, model, `MAX_USER_MESSAGES`, defaults. |
| `session.py` | Ensures all session state keys exist. |
| `prompts.py` | Interview system message + feedback prompt (`Overall Score` / `Feedback` format, `gpt-4o`). |
| `validation.py` | Checks that required fields are filled before starting. |
| `services/` | External integrations (OpenAI). |
| `ui/setup_form.py` | SET UP UI (`setup_complete`). |
| `ui/interview_chat.py` | INTERVIEW UI (`user_message_count`, `chat_complete`, `messages`). |
| `ui/feedback.py` | FEEDBACK UI (`feedback_show`, `messages`). |
| `.streamlit/secrets.toml` | Secrets loaded by Streamlit (`st.secrets`). |

---

## Session state keys

Defined in `config.SESSION_DEFAULTS`:

### SET UP

| Key | Purpose |
|---|---|
| `name`, `experience`, `skills` | Candidate profile text |
| `level`, `position`, `company` | Target role selections |
| `setup_complete` | `False` → show setup form; `True` → leave setup |

### INTERVIEW

| Key | Purpose |
|---|---|
| `user_message_count` | How many answers the candidate has sent |
| `chat_complete` | `True` when interview is finished |
| `messages` | Chat history (includes system message) |

### FEEDBACK

| Key | Purpose |
|---|---|
| `feedback_show` | `True` → show feedback screen |
| `messages` | Same transcript used to generate feedback |
| `feedback_text` | Cached AI feedback so it is not regenerated every rerun |

### Other

| Key | Purpose |
|---|---|
| `openai_model` | Model used for interview chat (`gpt-4o-mini` by default) |

Interview length is controlled by `MAX_USER_MESSAGES` in `config.py` (default: 5). Users can also click **End interview & get feedback** early.

Feedback uses `FEEDBACK_MODEL` (`gpt-4o`) and asks for:

```text
Overall Score: //Your score
Feedback: //Here you put your feedback
```

---

## Adding new code (keep this README updated)

When you add something, update this README in the same change:

| If you add… | Update… |
|---|---|
| A new Python module | Project structure tree + module table |
| A new UI screen/component | `ui/` section and flow under “How the app works” |
| A new stage or session flag | Stage diagram + session state tables |
| A new service (API, DB, etc.) | `services/` list and any setup steps |
| New config / env / secrets | Quick start or secrets section |
| New dependencies | Quick start install commands |

Goal: anyone opening `README.md` should understand the current layout without reading every file.

---

## Notes

- Do **not** commit real API keys. Keep `.streamlit/secrets.toml` local (or use env-based secrets in deployment).
- Billing / rate-limit errors from OpenAI are handled in `services/openai_service.py` and shown as clear UI messages (including “no balance”).
