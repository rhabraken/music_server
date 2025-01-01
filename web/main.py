import streamlit as st
import requests
import os
import re

# Load environment variables
SECRET_TOKEN = os.getenv("API_SECRET_TOKEN", "your-secret-token")
API_URL = os.getenv("API_URL", "http://localhost:5000/")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Qobuz Album Downloader",
    page_icon="🎵",
    layout="centered"
)

# App title and description
st.title("🎶 Qobuz Album Downloader")
st.markdown(
    """
    Welcome to the Qobuz Album Downloader! 🎧  
    Enter a Qobuz album URL below, and we'll start the download process for you.  
    """
)

# Input field for the URL
url = st.text_input(
    "Enter the Qobuz album URL:",
    placeholder="e.g., https://www.qobuz.com/us-en/album/let-it-be-the-beatles/123456789"
)

# Define the regex for URL validation
regex = r"^https:\/\/www\.qobuz\.com\/[a-zA-Z\-]+\/album\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9]+$"

# Button to send the URL to the API
if st.button("Start Download"):
    # Validate the URL format
    if not re.match(regex, url):
        st.error("❌ Invalid URL format. Please provide a valid Qobuz album URL.")
    elif not url.strip():
        st.error("❌ Please enter a URL.")
    else:
        # Prepare the headers and payload
        headers = {
            "Authorization": f"Bearer {SECRET_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"url": url}

        # Make the POST request
        with st.spinner("🚀 Sending your request to the server..."):
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.ok:
                    st.success("✅ Download started successfully! Enjoy your music! 🎶")
                else:
                    error_message = response.json().get("error", "Unknown error")
                    st.error(f"❌ Error: {error_message}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")

# Footer section
st.markdown(
    """
    ---
    💡 **Tip**: Make sure the album URL is valid and publicly accessible.  
    📖 [Learn more about Qobuz](https://www.qobuz.com)  
    """
)
