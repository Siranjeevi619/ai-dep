import os

import streamlit as st
from dotenv import load_dotenv
from groq import APIError
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq


TUTOR_PROMPT = """You are a patient, encouraging tutor. Use the conversation so
far to adapt to the learner's level, goals, and previous attempts. Explain ideas
in clear steps with concrete examples. For practice problems, start with a hint
or a guiding question. If the learner asks for a worked solution, show the
reasoning and answer. When helpful, end with one short check for understanding.
If you are unsure, say so. Reply in the learner's language.
"""

load_dotenv()
st.set_page_config(page_title="Study Tutor", page_icon="📚")
st.title("Study Tutor")
st.caption("Ask a question, work through a problem, or practice a topic.")

history = st.session_state.setdefault("history", [])
with st.sidebar:
    st.button("New chat", on_click=history.clear)
    st.caption("Your tutor remembers this chat while the session is open.")

for message in history:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.markdown(message.text)

api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    st.info("Set GROQ_API_KEY in your environment or .env file to start chatting.")

prompt = st.chat_input("What would you like to learn?", disabled=not api_key)
if prompt and prompt.strip():
    question = HumanMessage(content=prompt.strip())
    with st.chat_message("user"):
        st.markdown(question.text)

    with st.chat_message("assistant"), st.spinner("Thinking…"):
        tutor = ChatGroq(
            model=os.getenv("GROQ_MODEL", "").strip() or "openai/gpt-oss-20b",
            api_key=api_key,
            timeout=30,
        )
        try:
            reply = tutor.invoke([SystemMessage(content=TUTOR_PROMPT), *history, question])
        except APIError as error:
            status = getattr(error, "status_code", None)
            if status == 401:
                st.error("Groq rejected the API key. Check GROQ_API_KEY and try again.")
            elif status == 429:
                st.error("Groq's rate limit was reached. Wait a moment and try again.")
            else:
                st.error("Could not get a response from Groq. Check your connection and model, then try again.")
        else:
            if reply.text.strip():
                st.markdown(reply.text)
                history.extend([question, AIMessage(content=reply.text)])
            else:
                st.error("Groq returned an empty answer. Please try asking again.")
