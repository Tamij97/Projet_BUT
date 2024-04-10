import streamlit as st

from login import view_login
from signup import view_signup
from chatbot import view_chatbot
from Ressources.Session import initialize_session

def main():

    initialize_session()

    if st.session_state['current_page'] == 'Login' and st.session_state['user_is_connected'] == False:
        view_login()

    if st.session_state['current_page'] == 'Signup' and st.session_state['user_is_connected'] == False:
        view_signup()
    
    if st.session_state['current_page'] == 'Chatbot' and st.session_state['user_is_connected'] == True:
        view_chatbot()

if __name__ == "__main__":
    main()
