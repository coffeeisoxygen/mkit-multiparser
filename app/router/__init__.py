r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.router.rtr_admin import router as rtr_admin
from app.router.rtr_digipos import router as rtr_digipos


def setup_router(app):
    app.include_router(rtr_admin, prefix="/admin", tags=["admin"])
    app.include_router(rtr_digipos, prefix="/digipos", tags=["digipos"])
