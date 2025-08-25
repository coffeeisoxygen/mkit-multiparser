r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.api.v1.rtr_admin import router as rtr_admin
from app.api.v1.rtr_user import router as rtr_user

__all__ = ["rtr_admin", "rtr_user"]
