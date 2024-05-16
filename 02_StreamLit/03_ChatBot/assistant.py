import os
import dotenv
import streamlit as st
from database import insert_message, get_message
from groq import Groq
from models import Message

env = dotenv.load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ai_text_generate(user_message, select_model):
    if select_model == "Gemma-7B":
        model = "gemma-7b-it"
    elif select_model == "LLaMA3-8B":
        model = "llama3-8b-8192"
    elif select_model == "LLaMA3-70B":
        model = "llama3-70b-8192"
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_message,
        }
    ],

    model=model,
    temperature=0.5,
    max_tokens=8192,
    top_p=1,
    stream=False,
    )

    return chat_completion.choices[0].message.content


def process(user_message, user_id, model):
    ai_message = ai_text_generate(user_message, model)
    # add messages to database
    insert_message(type_message="user", text_message=user_message, user_id=user_id)
    insert_message(type_message="ai", text_message=ai_message, user_id=user_id)
    # add messages to list
    st.session_state.messages.append(Message(type="user", text=user_message, user_id=user_id))
    st.session_state.messages.append(Message(type="ai", text=ai_message, user_id=user_id))
    return ai_message


def ai_assistant(user_id, model):
    st.session_state.messages = get_message(user_id)

    for message in st.session_state.messages:
        with st.chat_message(message.type):
            st.markdown(message.text) 

    if user_text_message := st.chat_input("Send a message..."):
        with st.chat_message("user"):
            st.markdown(user_text_message)

        with st.spinner("Thinking..."):
            ai_message = process(user_text_message, user_id, model)
        with st.chat_message("ai"):
            st.markdown(ai_message)
