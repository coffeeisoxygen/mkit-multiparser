# from app.crud.crd_user import get_user_by_username, get_user_with_password_by_username
# from app.exception import UserNotFoundError, UserPasswordError
# from app.schemas.token.sch_token import (
#     TokenResponse,
#     UserLoginRequest,
#     UserLoginResponse,
# )
# from app.services.auth.token_service import TokenService
# from app.services.hasher.implement import Argon2Hasher
# from loguru import logger
# from sqlalchemy.ext.asyncio import AsyncSession


# class CredentialService:
#     """Service untuk verifikasi kredensial username dan password (direct CRUD)."""

#     def __init__(self, db_session: AsyncSession, hasher: Argon2Hasher | None = None):
#         """Inisialisasi CredentialService dengan dependency session dan hasher.

#         Args:
#             db_session (AsyncSession): SQLAlchemy async session.
#             hasher (Argon2Hasher, optional): Service untuk hash/verify password.
#         """
#         self.db_session = db_session
#         self.hasher = hasher or Argon2Hasher()
#         self.log = logger.bind(service="CredentialService")

#     async def authenticate(
#         self,
#         login_req: UserLoginRequest,
#         token_service: TokenService,
#     ) -> UserLoginResponse:
#         """Autentikasi user berdasarkan UserLoginRequest schema dan delegasi token ke TokenService.

#         Args:
#             login_req (UserLoginRequest): Schema request login user.
#             token_service (TokenService): Service untuk membuat JWT token.

#         Returns:
#             UserLoginResponse: Schema berisi user info dan token jika sukses.

#         Raises:
#             UserNotFoundError: Jika user tidak ditemukan.
#             UserPasswordError: Jika password salah.
#         """
#         user_model = await get_user_with_password_by_username(
#             self.db_session, login_req.username
#         )
#         if not user_model:
#             self.log.warning("User not found", username=login_req.username)
#             raise UserNotFoundError("User not found.")
#         # Verifikasi password
#         if not self.hasher.verify(login_req.password, user_model.hashed_password):
#             self.log.warning("Incorrect password", username=login_req.username)
#             raise UserPasswordError("Incorrect password.")
#         self.log.info("User authenticated successfully", username=login_req.username)
#         # Return UserRead schema for response
#         user_schema = get_user_by_username(self.db_session, login_req.username)
#         user = await user_schema
#         if user is None:
#             self.log.warning(
#                 "User not found after password verification",
#                 username=login_req.username,
#             )
#             raise UserNotFoundError("User not found after password verification.")
#         # Buat token JWT
#         temp_response = UserLoginResponse(
#             user=user,
#             is_active=getattr(user, "is_active", True),
#             is_superuser=getattr(user, "is_superuser", False),
#             token=TokenResponse(access_token="", token_type="bearer", expires_in=0),
#         )
#         jwt_token = token_service.create_token(temp_response)
#         token_response = TokenResponse(
#             access_token=jwt_token,
#             token_type="bearer",
#             expires_in=token_service.expire_minutes * 60,
#         )
#         return UserLoginResponse(
#             user=user,
#             is_active=getattr(user, "is_active", True),
#             is_superuser=getattr(user, "is_superuser", False),
#             token=token_response,
#         )
