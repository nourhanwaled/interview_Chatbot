# Chat Interview Project

Streamlit mock HR interview using **LangChain**. Default LLM provider is **Groq** (free tier, no OpenAI credits). OpenAI remains optional.

Stages: **SET UP → INTERVIEW → FEEDBACK**.

---

## Quick start (Groq — recommended)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a free API key at [console.groq.com/keys](https://console.groq.com/keys).

3. Add it to `.streamlit/secrets.toml` (see `secrets.toml.example`):

```toml
GROQ_API_KEY = "gsk_..."
```

4. Confirm `config.py` has:

```python
LLM_PROVIDER = "groq"
```

5. Run:

```bash
streamlit run app.py
```

### Optional: use OpenAI instead

```python
# config.py
LLM_PROVIDER = "openai"
```

```toml
# .streamlit/secrets.toml
OPEN_API_KEY = "sk-..."
```

---

## How the app works

```
SET UP  →  INTERVIEW  →  FEEDBACK
```

1. **SET UP** — profile + role; sets `setup_complete`.
2. **INTERVIEW** — LangChain streams replies (`ChatGroq` or `ChatOpenAI`).
3. **FEEDBACK** — LCEL chain `prompt | model | StrOutputParser` scores the transcript.

---

## Why Groq by default?

| Option | Pros | Cons |
|---|---|---|
| **Groq (default)** | Free tier, very fast, no local install | Needs free API key + rate limits |
| OpenAI | Strong models you already used | Requires paid credits |
| Ollama | Fully free/offline | Must install/run models on your PC |

---

## LangChain layout

| Piece | Role |
|---|---|
| `LLM_PROVIDER` in `config.py` | `"groq"` or `"openai"` |
| `ChatGroq` / `ChatOpenAI` | Active chat model |
| `dict_messages_to_langchain()` | Session dicts → LangChain messages |
| `get_feedback_prompt()` | Feedback `ChatPromptTemplate` |
| Feedback LCEL | `prompt \| model \| StrOutputParser` |
| Interview streaming | `model.stream(...)` → `st.write_stream` |

Default Groq models:

- Interview: `llama-3.1-8b-instant`
- Feedback: `llama-3.3-70b-versatile`

---

## Project structure

```
chat_interview_project/
├── app.py                         # Routes SET UP → INTERVIEW → FEEDBACK
├── config.py                      # Provider, models, form options, session defaults
├── session.py                     # Session state init
├── prompts.py                     # Prompt builders + ChatPromptTemplate
├── validation.py                  # Required-field checks
├── requirements.txt               # Dependencies (LangChain, Groq, OpenAI)
├── services/
│   ├── __init__.py
│   └── langchain_service.py       # Provider factory, streaming, feedback LCEL
├── ui/
│   ├── setup_form.py
│   ├── interview_chat.py
│   └── feedback.py
├── .streamlit/
│   ├── secrets.toml               # Local keys (gitignored)
│   └── secrets.toml.example       # Template for GROQ_API_KEY / OPEN_API_KEY
└── README.md
```

---

## Session state keys

| Key | Stage | Purpose |
|---|---|---|
| `name`, `experience`, `skills`, `level`, `position`, `company` | SET UP | Candidate profile |
| `setup_complete` | SET UP | Leave setup when `True` |
| `user_message_count`, `chat_complete`, `messages` | INTERVIEW | Progress + history |
| `feedback_show`, `feedback_text`, `messages` | FEEDBACK | Show + cache feedback |
| `llm_model` | all | Active interview model id |

Interview length: `MAX_USER_MESSAGES` (default 5), or **End interview & get feedback**.

Feedback format:

```text
Overall Score: //Your score
Feedback: //Here you put your feedback
```

---

## Notes

- Do **not** commit real API keys (`.streamlit/secrets.toml` is gitignored).
- Rate-limit / no-balance errors are handled in `services/langchain_service.py`.
