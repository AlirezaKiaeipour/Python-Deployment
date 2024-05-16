import re
import streamlit as st
import streamlit_authenticator as stauth
from database import insert_user, check_user, get_users, get_user_id
from assistant import ai_assistant

st.set_page_config(
    page_title="ChatBot",
    page_icon="💬",
    initial_sidebar_state="collapsed"
)


def check_valid(pattern,text):
    if re.match(pattern,text):
        return True
    else: 
        return False

def register():
    with st.form(key="register", clear_on_submit=True):
        st.subheader(":blue[Sign Up]")
        name = st.text_input("Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Repeat Password", type="password")
        btn_register = st.form_submit_button(":green[Sign Up]")

        if btn_register:
            if name:
                if password:
                    if confirm_password:
                        if email:
                            email_pattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
                            if check_valid(email_pattern, email):
                                if username:
                                    username_pattern = "^[a-zA-Z0-9]*$"
                                    if check_valid(username_pattern, username):
                                        if check_user(username=username, email=email):
                                            if password == confirm_password:
                                                insert_user(name=name, username=username, email=email, password=password)
                                                st.success("User Registered Successfully")
                                            else: st.warning("Passwords Do Not Match")
                                        else: st.warning("Username/Email Already Exists")
                                    else: st.warning("Invalid Username")
                                else: st.warning("Please Enter Username")
                            else: st.warning("Invalid Email")
                        else: st.warning("Please Enter Email")
                    else: st.warning("Please Confirm Password")
                else: st.warning("Please Enter Password")
            else: st.warning("Please Enter Your Name")


def main():
    st.sidebar.title(":green[ChatBot]")
    try:
        users = get_users()
        usernames = []
        emails = []
        passwords = []

        for user in users:
            usernames.append(user.username)
            emails.append(user.email)
            passwords.append(user.password)

        credentials = {"usernames": {}}

        for index in range(len(emails)):
            credentials["usernames"][usernames[index]] = {"name": emails[index], "password": passwords[index]}

        authenticator = stauth.Authenticate(credentials, cookie_name="chatbot", cookie_key="abcdef", cookie_expiry_days=7)
        email, st.session_state["authentication_status"], username = authenticator.login(fields={'Form name':':blue[Login]','Login':':green[Login]'},location="main")

        if not st.session_state["authentication_status"]:
            register()

        if username:
            if username in usernames:
                if st.session_state["authentication_status"]:
                    with st.sidebar:
                        st.sidebar.subheader(f":blue[Welcome {username}]")
                        model = st.selectbox("Choose model:",("Gemma-7B","LLaMA3-8B","LLaMA3-70B"))
                        authenticator.logout(button_name=":green[Logout]")

                    user_id = get_user_id(username)
                    ai_assistant(user_id, model)

                elif not st.session_state["authentication_status"]:
                    st.error("Incorrect Username or Password")
            else: st.warning("Username Does Not Exist, Please Sign Up")

    except:
        st.info("Refresh Page")


if __name__ == "__main__":
    main()