import requests

import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="X5 tech bot",
    page_icon="🤗",
)

# interact with FastAPI endpoint
QUESTION_URL = "http://localhost:5041/api/v1/get_answer"

st.balloons()

# construct UI layout
st.title(":green[X5 tech] bot")

st.header(
    "This X5 tech bot will help you with all your questions!"
)

import random
import time


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Sending request to API..."):
            data = requests.get(url=f"{QUESTION_URL}", params={"history": [{"role": "user","content": f"{prompt}"}]}).json()
            response = st.write_stream(data)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()