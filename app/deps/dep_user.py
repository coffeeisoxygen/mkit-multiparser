from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.deps.dep_service import get_token_service, get_user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service=Depends(get_token_service),
    user_service=Depends(get_user_service),
):
    """Ambil user dari JWT token."""
    payload = token_service.decode_token(token)
    user = await user_service.get_user_by_id(int(payload.sub))
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
