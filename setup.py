#!/usr/bin/env python3
"""
Installation and setup script for SQL Assistant
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Successfully installed all packages!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("🔧 Setting up environment file...")
        
        groq_key = input("Enter your Groq API key (or press Enter to skip): ").strip()
        
        env_content = f"""# GROQ API Configuration
GROQ_API_KEY={groq_key}

# Database Configuration (Optional - for custom databases)
# DATABASE_URL=sqlite:///your_database.db
# or for other databases:
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname
# DATABASE_URL=mysql://username:password@localhost:3306/dbname
"""
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ Environment file created!")
        
        if not groq_key:
            print("⚠️  Don't forget to add your Groq API key to the .env file!")
    else:
        print("✅ Environment file already exists!")

def create_sample_database():
    """Create the sample database"""
    print("🗃️ Creating sample database...")
    try:
        from create_sample_db import create_extended_sample_database
        create_extended_sample_database()
        print("✅ Sample database created successfully!")
    except Exception as e:
        print(f"❌ Error creating sample database: {e}")
        return False
    return True

def verify_installation():
    """Verify that everything is installed correctly"""
    print("🔍 Verifying installation...")
    
    try:
        import streamlit
        import langchain
        import pandas
        import plotly
        import sqlalchemy
        from langchain_groq import ChatGroq
        print("✅ All required packages are available!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 SQL Assistant Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create sample database
    create_sample_database()
    
    # Verify installation
    if not verify_installation():
        print("❌ Setup failed during verification")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your Groq API key to the .env file if you haven't already")
    print("2. Run the application: streamlit run app.py")
    print("3. Open your browser and start chatting with your database!")
    
    # Ask if user wants to run the app
    run_now = input("\nWould you like to run the application now? (y/n): ").lower().strip()
    if run_now in ['y', 'yes']:
        print("🚀 Starting SQL Assistant...")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Application stopped. You can restart it anytime with: streamlit run app.py")

if __name__ == "__main__":
    main()
