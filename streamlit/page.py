import os
import requests
import streamlit as st
import pandas as pd
import time
import json
import datetime
import extra_streamlit_components as stx

st.set_page_config(
    page_title="X5 tech bot",
    page_icon="🤗",
)

# Interact with FastAPI endpoint
QUESTION_URL = f"http://{os.getenv('SE_HOST')}:{os.getenv('SE_PORT')}/api/v1/get_answer"
COOKIE = "request_history"

st.title(":green[X5 tech] bot")
st.header("This X5 tech bot will help you with all your questions!")

cookie_manager = stx.CookieManager()
cookie = cookie_manager.get(cookie=COOKIE)
time.sleep(0.5)

if not isinstance(cookie, list):
    cookie = []

def response_generate():
    with st.spinner("Sending request to API..."):
        response = requests.post(
            url=f"{QUESTION_URL}", json={"history": st.session_state.messages}
        ).json()

    return response

def response_stream(answer):
    for word in answer:
        yield word
        time.sleep(0.02)

# Initialize session state for messages, sources, and visibility
if "messages" not in st.session_state:
    st.session_state.messages = cookie
    st.session_state.sources = []
    st.session_state.show_sources = {}

# Display chat messages from history on app rerun
for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Add button for assistant's messages to show/hide sources
        if message["role"] == "assistant" and "sources" in message:
            # Initialize visibility state for each message
            if index not in st.session_state.show_sources:
                st.session_state.show_sources[index] = False

            # Toggle button for showing/hiding sources
            if st.button(
                "Show Sources" if not st.session_state.show_sources[index] else "Hide Sources", 
                key=f"sources_button_{index}"
            ):
                st.session_state.show_sources[index] = not st.session_state.show_sources[index]

            # Display sources if the visibility state is True
            if st.session_state.show_sources[index]:
                for source in message["sources"]:
                    st.markdown(f"**Question:** {source['question']}")
                    st.markdown(f"**Content:** {source['content']}")
                    st.markdown(f"**Category:** {source['category']}")
                    st.divider()

# Accept user input
if prompt := st.chat_input("What is up?"):
    cookie.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp = response_generate()
        response = st.write_stream(response_stream(resp["qa_answer"]))
        sources = resp.get("sources", [])
        
        if sources:
            st.session_state.sources.append(sources)
            index = len(st.session_state.messages)  # Index for current message
            
            # Initialize visibility state for new message
            st.session_state.show_sources[index] = False

            # Toggle button for showing/hiding sources
            if st.button(
                "Show Sources" if not st.session_state.show_sources[index] else "Hide Sources", 
                key=f"sources_button_{index}"
            ):
                st.session_state.show_sources[index] = not st.session_state.show_sources[index]

            # Display sources if the visibility state is True
            if st.session_state.show_sources[index]:
                for source in sources:
                    st.markdown(f"**Question:** {source['question']}")
                    st.markdown(f"**Content:** {source['content']}")
                    st.markdown(f"**Category:** {source['category']}")
                    st.divider()

    cookie.append({"role": "assistant", "content": response, "sources": sources})
    st.session_state.messages.append({"role": "assistant", "content": response, "sources": sources})

    cookie_manager.set(COOKIE, cookie)

st.divider()
