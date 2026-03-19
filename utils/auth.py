
import streamlit as st



USER_DB = {
    "partner@vc.com": {"password": "123", "role": "Admin", "name": "Senior Partner"},
    "analyst@vc.com": {"password": "456", "role": "Analyst", "name": "Junior Analyst"}
}

def login_user(email, password):
    """Verifies credentials and sets session state."""
    if email in USER_DB and USER_DB[email]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_role = USER_DB[email]["role"]
        st.session_state.user_name = USER_DB[email]["name"]
        return True
    return False

def logout_user():
    """Clears session state and reloads."""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.messages = []
    st.rerun()