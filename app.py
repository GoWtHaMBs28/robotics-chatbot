import streamlit as st
import openai
from dotenv import load_dotenv
import os
from streamlit_chat import message
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are RoboTutor, expert in robotics & electronics. Provide:
1. Step-by-step instructions
2. Complete code with comments
3. Circuit diagrams (ASCII)
4. Component lists
5. Safety warnings
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

st.set_page_config(page_title="🤖 RoboTutor", page_icon="🤖", layout="wide")
st.title("🤖 RoboTutor - Robotics Chatbot")

# Chat history
for i, msg in enumerate(st.session_state.messages[1:]):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"{msg['role']}_{i}")

# Chat input
if prompt := st.chat_input("Ask about robotics projects..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            stream = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.empty()
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response.markdown(full_response + "▌")
            response.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar projects
with st.sidebar:
    st.header("🚀 Quick Projects")
    projects = ["Line Follower Robot", "Obstacle Avoider", "Bluetooth Car"]
    if project := st.selectbox("Pick one:", projects):
        st.button(f"📋 Tutorial: {project}", on_click=lambda: st.session_state.messages.append({"role": "user", "content": f"Complete tutorial for {project}"}))
