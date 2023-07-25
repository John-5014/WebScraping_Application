import streamlit as st
import streamlit_authenticator as stauth
from account import sign_up, fetch_users
import webbrowser
import time
# from dash import *


st.set_page_config(page_title='Authentication ', page_icon='📊', initial_sidebar_state='collapsed')

def login():
    
    
    try:
        users = fetch_users()
        emails = []
        usernames = []
        passwords = []

        for user in users:
            emails.append(user['key'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        credentials = {'usernames': {}}
        
        for index in range(len(emails)):
            
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

        email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

        info, info1 = st.columns(2)

        if not authentication_status:
            sign_up()

        if username:
            if username in usernames:
                if authentication_status:
                    # let User see app
                    st.sidebar.subheader(f'Welcome {username}')
                    st.sidebar.markdown("""
                            
                                ---
                                """)
                    Authenticator.logout('Log Out', 'sidebar')
            
                    
                    
                    

                    st.subheader('This is the home page')
                    
                    st.markdown(
                        """
                        ---
                        Created with ❤️ by Kaiser
                        
                        """
                        
                    )
                    if st.button("Proceed to next Page"):
                        
                        # Define the URL of the dashboard (dash.py) here
                        dashboard_url = "http://localhost:8501/"  # Update the URL as needed
                        with st.spinner('Hold it...'):
                            time.sleep(5)
                            st.success('See you on the next page 😍')
                        # Open the dashboard URL in the default web browser
                            webbrowser.open(dashboard_url)
                        
    

                    # st.button("Proceed to next Page")

                elif not authentication_status:
                    with info:
                        st.error('Incorrect Password or username')
                else:
                    with info:
                        st.warning('Please feed in your credentials')
            else:
                with info:
                    st.warning('Username does not exist, Please Sign up')


    except:
        
        st.success('Refresh Page')
login()