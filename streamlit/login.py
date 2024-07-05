import streamlit as st
from PIL import Image

# Set the page title and icon
st.set_page_config(page_title="Instagram Login", page_icon="📸")

# Load the Instagram logo
#logo = Image.open("instagram_logo.png")

# Create the login form
#st.image(logo, width=200)
st.title("Instagram")

with st.form(key="login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Log In")

if submit_button:
    if username == "your_username" and password == "your_password":
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")
