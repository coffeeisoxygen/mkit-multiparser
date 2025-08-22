@echo off
REM Sincronisasi dependensi dengan uv...

echo Sincronisasi dependensi dengan uv...
uv sync

REM sinkronisasi database dengan alembic
echo Sincronisasi database dengan alembic...
uv run alembic upgrade head

REM supply environment variables
set UVICORN_HOST=0.0.0.0
set UVICORN_PORT=8000

REM Menjalankan server uvicorn
echo Menjalankan server FastAPI...
uv run uvicorn main:app --host=%UVICORN_HOST% --port=%UVICORN_PORT% --workers=4 --log-level=info

pause
