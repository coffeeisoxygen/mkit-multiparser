from app.exception import AuthError
from app.schemas import UserLoginRequest, UserLoginResponse, UserToken
from app.services.auth.credential_service import CredentialService
from app.services.auth.token_service import TokenService


class AuthService:
    """Facade: login → token, token → user info (stateless, dari JWT payload)."""

    def __init__(
        self,
        credential_service: CredentialService,
        token_service: TokenService,
    ):
        self.cred = credential_service
        self.token = token_service

    async def login(self, username: str, password: str) -> UserLoginResponse:
        """Login user, return UserLoginResponse (berisi JWT token dan user info).

        Args:
            username (str): Username user.
            password (str): Password plain user.

        Returns:
            UserLoginResponse: berisi user info dan JWT token.
        """
        login_req = UserLoginRequest(username=username, password=password)
        response = await self.cred.authenticate(login_req, self.token)
        return response

    def get_user_from_token(self, token: str) -> UserToken:
        """Ambil info user dari JWT token (tanpa query DB).

        Args:
            token (str): JWT token string.

        Returns:
            UserToken: Info user dari payload JWT.
        """
        payload = self.token.decode_token(token)
        try:
            id_val = payload.get("id")
            if id_val is None:
                raise AuthError("Token payload missing 'id' field")  # noqa: TRY301
            # "sub" is username (str)
            return UserToken(
                id=int(id_val),
                username=payload.get("username") or payload.get("sub") or "",
                email=payload.get("email") or "",
                full_name=payload.get("full_name") or "",
                is_superuser=payload.get("is_superuser", False),
                is_active=payload.get("is_active", True),
            )
        except Exception as e:
            raise AuthError(f"Invalid token payload: {e}") from e
