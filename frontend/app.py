import streamlit as st
import requests

st.markdown("<h1 style='color: #40E0D0;'>Meowsterpiece: Your personal C(h)atBot 🐱</h1>", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def send_message(user_message):
    response = requests.post("http://localhost:5000/ask", json={"message": user_message})
    if response.status_code == 200:
        return response.json().get("response")
    return "Error: Unable to get a response."


chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div style='text-align: right; color: #ff9800; margin: 5px 0;'><strong>User:</strong> {message['content']} 😊</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; margin: 5px 0;'><strong>Assistant:</strong> {message['content']} 🤖</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your message:", "")


if st.button("Send"):
    if user_input:

        st.session_state.messages.append({"role": "user", "content": user_input})
        assistant_response = send_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.experimental_rerun()

st.markdown("<style>div.stTextInput { margin-top: 20px; }</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton>button {
            background-color: #ff9800;
            color: white;
        }
        .stButton>button:hover {
            background-color: #e68a00;
        }
        .main {
            padding: 0; /* Remove padding */
        }
        .stTextInput {
            margin-left: 0; 
            margin-right: 0; 
        }
    </style>
""", unsafe_allow_html=True)
