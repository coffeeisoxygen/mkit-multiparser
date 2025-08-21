@echo off


REM Activate the virtual environment
call .venv\Scripts\activate
set APP_ENV=DEVELOPMENT
REM Run Uvicorn with custom log config and log level
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload  --log-level=info


pause
