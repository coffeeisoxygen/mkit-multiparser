"""service layer basic user operations."""

from app.crud.cr_user import UserCRUD
from app.exception import UserDuplicateError
from app.schemas import UserInDB
from app.schemas.user import UserCreate
from app.services.hasher.implement import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    @staticmethod
    async def register(session: AsyncSession, register_data: UserCreate) -> "UserInDB":
        """Register new user - uses UserCRUD."""
        existing_user = await UserCRUD.get_by_username(
            session=session, username=register_data.username
        )
        if existing_user:
            raise UserDuplicateError(
                message="Username already exists",
                context={"username": register_data.username},
            )

        existing_email = await UserCRUD.get_by_email(session, register_data.email)
        if existing_email:
            raise UserDuplicateError(
                message="Email already exists", context={"email": register_data.email}
            )

        # Hash the password and pass as 'password'
        hasher = Argon2Hasher()
        hashed_pw = hasher.hash(register_data.password)

        return await UserCRUD.create(
            session,
            username=register_data.username,
            email=register_data.email,
            full_name=register_data.full_name,
            hashed_password=hashed_pw,
        )

    async def get_user(self, session: AsyncSession, user_id: str) -> "UserInDB | None":
        """Get user by ID - uses UserCRUD."""
        return await UserCRUD.get(session=session, user_id=user_id)

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> "UserInDB | None":
        """Get user by username - uses UserCRUD."""
        return await UserCRUD.get_by_username(session=session, username=username)

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> "UserInDB | None":
        """Get user by email - uses UserCRUD."""
        return await UserCRUD.get_by_email(session=session, email=email)
