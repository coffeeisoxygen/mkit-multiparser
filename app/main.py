import uvicorn
from app.config import get_settings
from fastapi import FastAPI

settings = get_settings()
app = FastAPI()


if __name__ == "__main__":
    # just in developement to enable run uv run app\main.py
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
