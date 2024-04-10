import streamlit as st
import requests
from Ressources.Config import URL
from Ressources.Translations import translations


def view_signup():
    Global = translations[st.session_state['languages']]
    signup = translations[st.session_state['languages']]['signupPage']

    st.title(signup['signup'])
    st.write(signup['description'])

    username = st.text_input(Global["username"], key='username')
    password = st.text_input(Global["password"], type="password", key='password')

    signup_disabled = not username or not password
    st.button(signup['signup'], on_click=function_signup_button_pressed, disabled=signup_disabled)

    col1, col2, col3 = st.sidebar.columns([3, 1, 1])
    col1.write(Global['language'])
    col2.button('EN ', on_click=function_set_language, args=('en',))
    col3.button('FR ', on_click=function_set_language, args=('fr',))
    
    col1, col3 = st.sidebar.columns([4, 1])
    col1.write(signup['connectAccount'])
    col3.button("👋", on_click=function_login_button_pressed)


def function_set_language(locale):
    st.session_state['language'] = locale


def function_signup_button_pressed():
    response = requests.post(URL + "signup", json={
        'username': st.session_state['username'],
        'password': st.session_state['password']
    })
    message = response.json().get('message', '')

    if response.status_code == 200:
        st.success(message)
        st.session_state['current_page'] = 'Login'
        st.session_state['signup_pressed'] = True
        st.session_state['username'] = None
        st.session_state['password'] = None
    else:
        st.error(message)


def function_login_button_pressed():
    st.session_state['current_page'] = 'Login'
    st.session_state['login_pressed'] = True