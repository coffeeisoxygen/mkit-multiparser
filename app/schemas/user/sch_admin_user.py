"""Schema khusus untuk admin user."""

from app.schemas.user.sch_user import UserBase, UserRead


class UserSeedAdmin(UserBase):
    is_superuser: bool
    is_active: bool


class UserAdminRead(UserRead):
    is_superuser: bool
