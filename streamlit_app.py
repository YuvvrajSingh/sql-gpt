# Main entry point for Streamlit Cloud deployment
# This file ensures Streamlit Cloud uses the correct deployment version

import streamlit as st

# MUST be first Streamlit command
st.set_page_config(
    page_title="Enhanced SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# Now import and run the main app
from app_deploy import main

if __name__ == "__main__":
    main()

# Auto-run for Streamlit Cloud
main()
