# app/utils.py
import os
from dotenv import load_dotenv
import streamlit as st

def load_environment():
    """Loads and verifies that the required API keys are present."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🚨 GOOGLE_API_KEY is missing! Check your .env file.")
        st.stop()
    return api_key

def format_transfer_update(response_text):
    """
    A helper to post-process the LLM output.
    Adds a 'Verified by Romano' signature.
    """
    signature = "\n\n---\n*Verified Update | Fabrizio Romano AI Bot ⚽*"
    return f"{response_text}{signature}"

def check_here_we_go(text):
    """
    Checks if the response contains the signature catchphrase 
    to trigger a special UI effect in Streamlit.
    """
    return "HERE WE GO" in text.upper()