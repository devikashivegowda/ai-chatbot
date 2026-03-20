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

def logout_user(cookies): 
    """Clears session state and deletes browser cookies."""
    import streamlit as st
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_name = ""
    st.session_state.user_role = ""
    st.session_state.messages = []
    
    if "user_email" in cookies:
        del cookies["user_email"]
        cookies.save()
        
    st.rerun()


def login_as_guest():
    """Initializes a temporary guest session."""
    st.session_state.logged_in = True
    st.session_state.user_email = "guest@neostats.com"
    st.session_state.user_name = "Guest Recruiter"
    st.session_state.user_role = "Recruiter (Guest)"
    st.session_state.messages = [] 
    return True