r"""configurasi router dan lain lain exposed disini.

include registering the routers
"""

from app.api.v1.rtr_admin import router as rtr_admin
from app.api.v1.rtr_digipos import router as rtr_digipos

__all__ = ["rtr_admin", "rtr_digipos"]
