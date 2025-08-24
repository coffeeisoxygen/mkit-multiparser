"""service layer basic user operations."""

from app.crud.cr_user import UserCRUD
from app.exception import UserDuplicateError
from app.schemas import UserInDB
from app.schemas.token import TokenResponse
from app.schemas.token.sch_token import UserLoginRequest, UserLoginResponse
from app.schemas.user import UserCreate
from app.services.auth.token_service import TokenService
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
            session=session,
            username=register_data.username,
            email=register_data.email,
            full_name=register_data.full_name,
            hashed_password=hashed_pw,
        )

    @staticmethod
    async def login(
        session: AsyncSession,
        login_data: UserLoginRequest,
        token_service: TokenService,
    ) -> UserLoginResponse:
        """Authenticate user and return token + user data.

        Args:
            session (AsyncSession): Database session.
            login_data (UserLoginRequest): Login request data.
            token_service (TokenService): Token service for JWT creation.

        Returns:
            UserLoginResponse: User data and token.

        Raises:
            ValueError: If username or password is invalid.
        """
        user = await UserCRUD.get_by_username(session, login_data.username)
        if not user:
            raise ValueError("Invalid username or password")

        hasher = Argon2Hasher()
        if not hasher.verify(login_data.password, user.hashed_password):
            raise ValueError("Invalid username or password")

        access_token = token_service.create_token(
            user_id=user.id,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

        token = TokenResponse(
            access_token=access_token,
            expires_in=token_service.expire_minutes * 60,
        )

        return UserLoginResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            token=token,
        )

    @staticmethod
    async def get_user(session: AsyncSession, user_id: str) -> "UserInDB | None":
        """Get user by ID - uses UserCRUD."""
        return await UserCRUD.get(session=session, user_id=user_id)

    @staticmethod
    async def get_by_username(
        session: AsyncSession, username: str
    ) -> "UserInDB | None":
        """Get user by username - uses UserCRUD."""
        return await UserCRUD.get_by_username(session=session, username=username)

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> "UserInDB | None":
        """Get user by email - uses UserCRUD."""
        return await UserCRUD.get_by_email(session=session, email=email)
