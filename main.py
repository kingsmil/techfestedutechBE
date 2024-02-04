import streamlit as st
from assistant import OpenAIAssistant
st.set_page_config(layout="wide")
ai= OpenAIAssistant()



if "messages" not in st.session_state:
    st.session_state.messages=[
        {
            "role":"Assistant",
            "content": "Welcome to the NTUtor! Ask any questions you would require here!"
        }
    ]
if "user_input" not in st.session_state:
    st.session_state.user_input=None

if "current_question" not in st.session_state:
    st.session_state.current_question=None
    
if "MH1100" not in st.session_state:
    st.session_state.MH1100=False

def send_message_callback():
    if st.session_state.user_input=="":return
    if st.session_state.user_input is None :return
    st.session_state.messages.append({
        "role":'User',
        "content": st.session_state.user_input
        })
    new_message = ai.generate_response("Answer MH1100:"+st.session_state.user_input, "128", "Moe")
    st.session_state.messages.append({
        "role":'Assistant',
        "content": new_message
    })
    st.session_state.user_input=None

def generate_question():
    if st.session_state.MH1100=="":return
    if st.session_state.MH1100 is None :return
    st.session_state.current_question = ai.generate_response("Generate 1:MH1100", "128", "Jun Hong")
    

tab1, tab2, tab3 = st.tabs(["MH1100", "MH1812", "SC1003"])
with st.container():
    with tab1:
        st.header("MH1100")
        st.button("Generate a question",key="MH1100",on_click=generate_question())
        if st.session_state.MH1100:
            st.markdown(
                f"<div style=' padding: 10px; border-radius:10px;margin-bottom:10px;'>"
                f"<b>Question:</b>{st.session_state.current_question}</div>",
                unsafe_allow_html=True
            )
    with tab2: 
        st.header("MH1812")
        question=st.button("Generate a question",key="MH1812")
        if question:
            test=True
            st.title("The question is below")
    with tab3: 
        st.header("SC1003")
        question=st.button("Generate a question",key="SC1003")
        if question:
            st.title("The question is below")

with st.sidebar:
    st.title("Your friendly helper!")
    st.text_input("Your message:",key="user_input",on_change=send_message_callback())
    with st.container():
        for message in reversed(st.session_state.messages):
            role=message["role"].capitalize()
            content=message["content"]
            if role=="User":color="#3AB54A"
            else: color="#F63366"

            st.markdown(
                f"<div style='background-color: {color}; padding: 10px; border-radius:10px;margin-bottom:10px;'>"
                f"<b>{role}:</b>{content}</div>",
                unsafe_allow_html=True
            )

            st.write("""
                     <style>
                     .block-container{
                         height:90vh;
                         overflow:scroll
                     }
                     </style>
                     """, unsafe_allow_html=True)

