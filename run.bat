@echo off
:: Set terminal colors: 60 = Yellow Background, Black Text
color 60
title Launching AI Resume Screening App...

echo ===================================================
echo     Launching AI Resume Screening App...
echo ===================================================
echo.

:: 1. Check if virtual environment exists; if not, create it
if not exist "venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Error: Python was not found or failed to create venv.
        pause
        exit /b 1
    )
    echo [+] Virtual environment created successfully.
    echo.
)

:: 2. Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

:: 3. Check and install missing dependencies
echo [*] Checking and installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [X] Error: Failed to install requirements.
    pause
    exit /b 1
)
echo [+] Dependencies are up to date.
echo.

:: 4. Check for .env file
if not exist ".env" (
    echo [!] Warning: .env file not found.
    echo [!] Creating a template .env file...
    echo OPENAI_API_KEY=your_actual_api_key_here > .env
    echo [!] Please update the .env file with your actual OpenAI API key!
    echo.
)

:: 5. Launch Streamlit Application
echo ===================================================
echo     Starting Streamlit Server...
echo ===================================================
echo.
streamlit run app.py

pause