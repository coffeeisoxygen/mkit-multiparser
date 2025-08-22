r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.api.v1 import rtr_admin, rtr_digipos


def setup_router(app):
    app.include_router(rtr_admin, prefix="/admin", tags=["admin"])
    app.include_router(rtr_digipos, prefix="/digipos", tags=["digipos"])
