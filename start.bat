@echo off
echo Starting FastAPI MVC Development Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing/Updating requirements...
pip install -r requirements.txt

REM Initialize database if not exists
if not exist "app.db" (
    echo Initializing database...
    python init_db.py
)

REM Start the application
echo.
echo Starting FastAPI application...
echo API Documentation will be available at: http://localhost:8000/docs
echo Application will be available at: http://localhost:8000
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
