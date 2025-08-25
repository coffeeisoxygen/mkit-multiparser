# """Dependency provider for user-related services (UserAuthService)."""

# from app.database.core.session import sessionmanager
# from app.database.repositories.repo_user import UserRepository
# from app.services.session.srv_session import SessionService
# from app.services.token.srv_token import TokenService
# from app.services.user.srv_user_register import UserService
# from app.utils.hasher.argon2 import Argon2Hasher


# async def get_user_auth_service() -> UserService:
#     """Dependency provider for UserAuthService.

#     Returns:
#         UserAuthService: Instance with all dependencies injected.
#     """
#     async with sessionmanager.session() as db_session:
#         user_repo = UserRepository(db_session)
#         hasher = Argon2Hasher()
#         session_service = SessionService(...)  # isi dengan repo session yang sesuai
#         token_service = TokenService(...)  # isi dengan config/token yang sesuai
#         return UserService(
#             user_repo=user_repo,
#             hasher=hasher,
#             session_service=session_service,
#             token_service=token_service,
#         )
