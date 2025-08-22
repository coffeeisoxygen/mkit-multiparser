r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.router import rtr_admin


def setup_router(app):
    app.include_router(rtr_admin.router, prefix="/admin", tags=["admin"])
