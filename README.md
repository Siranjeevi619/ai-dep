# Study Tutor

A Streamlit chatbot that uses LangChain's `ChatGroq` integration to explain topics, guide learners through practice problems, and answer follow-up questions. The full conversation stays in memory for the active Streamlit session. **New chat** clears it, and reloading the browser starts a fresh session.

## Run locally

Use Python 3.10 or newer and `uv`. From PowerShell, install the dependencies and create your local configuration.

```powershell
uv venv
uv pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your [Groq API key](https://console.groq.com/keys) to `.env`, then start the app.

```powershell
.venv/Scripts/python.exe -m streamlit run app.py
```

The default model is `openai/gpt-oss-20b`. Set `GROQ_MODEL` in `.env` to use a different model available to your Groq account.

## Run with Docker

Create `.env` from `.env.example` and fill in `GROQ_API_KEY` before starting the container.

```powershell
docker build -t study-tutor .
docker run --rm --env-file .env -p 127.0.0.1:8501:8501 study-tutor
```

Open [Study Tutor](http://localhost:8501). Docker loads `.env` when the container starts, and `.dockerignore` keeps it out of the build context.

At startup, the container installs `requirements.txt` for its non-root user before launching Streamlit. Each fresh container needs access to PyPI and enough startup time to finish the install. In the cloud, set `GROQ_API_KEY` through the service's runtime environment settings. Streamlit listens on `PORT` when provided and defaults to `8501`.
