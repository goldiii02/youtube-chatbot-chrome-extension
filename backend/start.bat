@echo off
echo Starting YouTube Chatbot Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copy env.example to .env and add your API keys.
    echo.
    pause
)

REM Start server
echo.
echo Starting FastAPI server...
echo Server will be available at http://localhost:8000
echo Press Ctrl+C to stop
echo.
python main.py

