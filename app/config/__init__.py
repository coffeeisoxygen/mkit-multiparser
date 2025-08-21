from app.config.core import get_settings
from app.config.custom.lifespan import app_lifespan
from app.config.custom.cors import setup_cors

__all__ = ("get_settings", "app_lifespan", "setup_cors")
