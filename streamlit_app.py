# Main entry point for Streamlit Cloud deployment
# This file ensures Streamlit Cloud uses the correct deployment version

from app_deploy import main

if __name__ == "__main__":
    main()

# Auto-run for Streamlit Cloud
main()
