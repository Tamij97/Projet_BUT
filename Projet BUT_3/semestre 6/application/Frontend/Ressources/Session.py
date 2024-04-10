import streamlit as st

def initialize_session():
    # APP
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Login'

        
    # LOGIN
    if 'login_pressed' in st.session_state:
        st.session_state['login_pressed'] = False 

    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    if 'user_name' not in st.session_state:
        st.session_state['user_id'] = None
        
    if 'user_is_connected' not in st.session_state:
        st.session_state['user_is_connected'] = False


    # SIGNUP
    if 'signup_pressed' in st.session_state:
        st.session_state['signup_pressed'] = False 


    # CHAT
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = {}
    
    if 'selected_chat' not in st.session_state:
        st.session_state['selected_chat'] = {}

    if 'user_question' not in st.session_state:
        st.session_state['user_question'] = ''

    if 'chat_id' not in st.session_state:
        st.session_state['chat_id'] = None

    if 'file_content' not in st.session_state:
        st.session_state['file_content'] = ''
    
    if 'have_file' not in st.session_state:
        st.session_state['have_file'] = False
    
    if 'model_selected' not in st.session_state:
        st.session_state['model_selected'] = None

    if 'model_selected_bln' not in st.session_state:
        st.session_state['model_selected_bln'] = False

    if 'languages' not in st.session_state:
        st.session_state['languages'] = "en"
