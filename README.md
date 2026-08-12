# Chat Interview Project

Streamlit app that runs a mock HR interview with **LangChain + OpenAI** across three stages: **SET UP → INTERVIEW → FEEDBACK**.

---

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
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
2. **INTERVIEW** — LangChain streams replies from `ChatOpenAI` using the chat history in `messages`.
3. **FEEDBACK** — an LCEL chain (`prompt | model | StrOutputParser`) scores the transcript.

---

## LangChain layout

| Piece | Role |
|---|---|
| `langchain_openai.ChatOpenAI` | Interview + feedback LLMs |
| `dict_messages_to_langchain()` | Converts session dicts → LangChain messages |
| `get_feedback_prompt()` | `ChatPromptTemplate` for feedback |
| Feedback LCEL | `prompt \| ChatOpenAI(gpt-4o) \| StrOutputParser` |
| Interview streaming | `ChatOpenAI.stream(...)` → `st.write_stream` |

---

## Project structure

```
chat_interview_project/
├── app.py                         # Entry point: routes SET UP → INTERVIEW → FEEDBACK
├── config.py                      # Constants, option lists, session defaults
├── session.py                     # Initialize Streamlit session state
├── prompts.py                     # Prompt builders + LangChain ChatPromptTemplate
├── validation.py                  # Form field validation helpers
├── requirements.txt               # Python dependencies (incl. LangChain)
├── services/
│   ├── __init__.py
│   └── langchain_service.py       # ChatOpenAI, stream interview, feedback LCEL chain
├── ui/
│   ├── __init__.py
│   ├── setup_form.py              # SET UP stage UI
│   ├── interview_chat.py          # INTERVIEW stage UI
│   └── feedback.py                # FEEDBACK stage UI
├── .streamlit/
│   └── secrets.toml               # Local secrets (API key) — do not commit real keys
└── README.md
```

### Module responsibilities

| File / folder | Responsibility |
|---|---|
| `app.py` | Thin entry point. Routes by stage flags. |
| `config.py` | Titles, models, `MAX_USER_MESSAGES`, defaults. |
| `session.py` | Ensures all session state keys exist. |
| `prompts.py` | Interview/feedback prompt text + LangChain templates. |
| `validation.py` | Required-field checks before starting. |
| `services/langchain_service.py` | LangChain LLMs, streaming, feedback chain, rate-limit UI. |
| `ui/setup_form.py` | SET UP UI (`setup_complete`). |
| `ui/interview_chat.py` | INTERVIEW UI (`user_message_count`, `chat_complete`, `messages`). |
| `ui/feedback.py` | FEEDBACK UI (`feedback_show`, `messages`). |

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
| `openai_model` | Interview model (`gpt-4o-mini` by default) |

Interview length: `MAX_USER_MESSAGES` in `config.py` (default: 5), or **End interview & get feedback**.

Feedback model: `FEEDBACK_MODEL` (`gpt-4o`), format:

```text
Overall Score: //Your score
Feedback: //Here you put your feedback
```

---

## Adding new code (keep this README updated)

| If you add… | Update… |
|---|---|
| A new Python module | Project structure tree + module table |
| A new UI screen/component | `ui/` section and “How the app works” |
| A new stage or session flag | Stage diagram + session state tables |
| A new LangChain chain/service | LangChain layout + `services/` |
| New dependencies | `requirements.txt` + Quick start |

---

## Notes

- Do **not** commit real API keys.
- Rate-limit / no-balance errors are handled in `services/langchain_service.py`.
