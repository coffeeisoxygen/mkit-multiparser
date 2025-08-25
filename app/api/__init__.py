r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.api.v1 import rtr_admin, rtr_user


def setup_router(app):
    app.include_router(rtr_admin, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(rtr_user, prefix="/api/v1/user", tags=["user"])
