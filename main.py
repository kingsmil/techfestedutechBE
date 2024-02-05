import json
import streamlit as st
from assistant import OpenAIAssistant
st.set_page_config(layout="wide")
ai = OpenAIAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "Assistant",
            "content": "Welcome to the NTUtor! Ask any questions you would require here!"
        }
    ]
submitted=False
if "user_input" not in st.session_state:
    st.session_state.user_input = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

def send_message_callback():
    if st.session_state.user_input == "": return
    if st.session_state.user_input is None: return
    st.session_state.messages.append({
        "role": 'User',
        "content": st.session_state.user_input
    })
    new_message = ai.generate_response("Answer MH1100:" + st.session_state.user_input, "116", "Moe")
    st.session_state.messages.append({
        "role": 'Assistant',
        "content": new_message
    })
    st.session_state.user_input = None


def generate_question():
    st.session_state.current_question = ai.extract_json(ai.generate_response("Generate 1:MH1100", "116", "Jun Hong"))

def answer_question(answer):
    temp={
        "question":st.session_state.current_question['question'],
        "answer":st.session_state.current_question['answer'],
        "user_answer": answer
    }
    temp2=json.dumps(temp)
    print(temp2)
    test=ai.generate_response(temp2, "116", "Jun Hong")
    print("test:",test)
    return test

tab1, tab2, tab3 = st.tabs(["MH1100", "MH1812", "SC1003"])

with st.container():
    with tab1:
        st.header("MH1100")
        if st.button("Generate a question", key="MH1100"):
            with st.spinner("Training ongoing"):
                generate_question()
        if st.session_state.current_question:
            with st.form("question_answer"):
                st.markdown(
                    f"<div style=' padding: 10px; border-radius:10px;margin-bottom:10px;'>"
                    f"<b>Question: </b>{st.session_state.current_question['question']}</div>",
                    unsafe_allow_html=True
                )
                answer = st.text_area("Answer goes here")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    # submit answer goes here
                    print(answer)
                    aianswer = answer_question(answer)
                    print(aianswer)
                    st.write("Feedback:", aianswer)
    with tab2:
        st.header("MH1812")
        question = st.button("Generate a question", key="MH1812")
        if question:
            test = True
            st.title("The question is below")
    with tab3:
        st.header("SC1003")
        question = st.button("Generate a question", key="SC1003")
        if question:
            st.title("The question is below")

with st.sidebar:
    st.title("Your friendly helper!")
    st.text_input("Your message:", key="user_input", on_change=send_message_callback())
    with st.container():
        for message in reversed(st.session_state.messages):
            role = message["role"].capitalize()
            content = message["content"]
            if role == "User":
                color = "#3AB54A"
            else:
                color = "#F63366"

            with st.chat_message(message["role"]):
                st.markdown(message["content"])
