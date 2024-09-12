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

# interact with FastAPI endpoint
QUESTION_URL = "http://search_engine:5041/api/v1/get_answer"
COOKIE = "request_history"

#st.balloons()

# construct UI layout
st.title(":green[X5 tech] bot")

st.header(
    "This X5 tech bot will help you with all your questions!"
)

#@st.cache_resource
#def get_manager():
#    return stx.CookieManager()

cookie_manager = stx.CookieManager()
#print(cookie_manager)
cookie = cookie_manager.get(cookie=COOKIE)
time.sleep(0.5)

if  not isinstance(cookie, list):
    cookie = []


# Streamed response emulator
def response_generate():
    with st.spinner("Sending request to API..."):
        response = requests.post(url=f"{QUESTION_URL}", json={"history": st.session_state.messages}).json()
    for word in response["qa_answer"]:
        yield word
        time.sleep(0.02)



if "messages" not in st.session_state:
    st.session_state.messages = cookie

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    #st.session_state.messages.append({"role": "user", "content": prompt})
    #cookie = cookie_manager.get(cookie=COOKIE)
    cookie.append({"role": "user", "content": prompt})
    
    #cookie_manager.delete(COOKIE)
    #cookie_manager.set(COOKIE, cookie)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):     
        response = st.write_stream(response_generate())

    # Add assistant response to chat history

    #cookie = cookie_manager.get(cookie=COOKIE)
    cookie.append({"role": "assistant", "content": response})
    #cookie_manager.delete(COOKIE)
    #cookie_manager.set(COOKIE, cookie)
    st.session_state.messages.append({"role": "assistant", "content": response})

    #cookie_manager.delete(COOKIE)
    cookie_manager.set(COOKIE, cookie)
st.divider()



# Initialize chat history
#cookies = cookie_manager.get_all()
#st.write(cookies)



#cookies = cookie_manager.get_all()

