@echo off
REM Ecoreborn Website - Windows Setup Script
REM This script automates the initial setup process

echo ========================================
echo Ecoreborn Website Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from python.org
    pause
    exit /b 1
)

echo [1/6] Checking Python version...
python --version

echo.
echo [2/6] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv .venv
    echo Virtual environment created successfully
)

echo.
echo [3/6] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/6] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [5/6] Setting up environment configuration...
if exist .env (
    echo .env file already exists, skipping
) else (
    copy .env.example .env
    echo .env file created. Please edit it with your MongoDB credentials.
)

echo.
echo [6/6] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Edit .env file and add your MongoDB Atlas credentials
echo 2. Run: python init_db.py
echo 3. Run: python app.py
echo 4. Open http://localhost:5000 in your browser
echo.
echo Default admin credentials:
echo   Email: admin@ecoreborn.example
echo   Password: Ec0r3b0rn!
echo.
echo ========================================
echo.
pause
