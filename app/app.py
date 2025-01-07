from openai import OpenAI
import streamlit as st
from src.services.openai_service import OpenAIService
from src.config.settings import Settings
from dotenv import load_dotenv

load_dotenv()

settings = Settings()
openai_service = OpenAIService()


st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = openai_service.process_message(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
