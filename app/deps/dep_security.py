from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database.repositories.intf_user import IUserRepository
from app.services.token.intf_token import ITokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: ITokenService = Depends(),
    user_repo: IUserRepository = Depends(),
):
    """Ambil user dari JWT token."""
    payload = token_service.decode_token(token)
    user = user_repo.get_user_with_id(int(payload.sub))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_is_active_user(current_user=Depends(get_current_user)):
    """Pastikan user aktif."""
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_is_admin_user(current_user=Depends(get_current_user)):
    """Pastikan user adalah admin."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not admin")
    return current_user
