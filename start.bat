@echo off
echo 🚀 Starting SQL Assistant...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist "venv\Lib\site-packages\streamlit" (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
)

REM Create sample database if it doesn't exist
if not exist "sample_data.db" (
    if not exist "extended_sample_data.db" (
        echo 🗃️ Creating sample database...
        python create_sample_db.py
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Environment file not found. Creating template...
    echo # GROQ API Configuration > .env
    echo GROQ_API_KEY=your_groq_api_key_here >> .env
    echo.
    echo Please add your Groq API key to the .env file
)

echo.
echo 🌟 Launching SQL Assistant...
echo Open your browser to http://localhost:8501
echo.

REM Start the Streamlit application
streamlit run app.py

echo.
echo 👋 SQL Assistant stopped
pause
