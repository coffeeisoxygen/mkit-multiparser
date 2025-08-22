import httpx
from loguru import logger
from pydantic import BaseModel

from app.config import get_settings

settings = get_settings()


class DigiposApiResponse(BaseModel):
    req: dict
    res: str


class DigiposApiClient:
    """Client untuk konsumsi OtomaX API."""

    BASE_URL = settings.DGP.baseurl.rstrip("/")
    USERNAME = settings.DGP.username
    PASSWORD = settings.DGP.password
    PIN = settings.DGP.pin

    async def _get(self, endpoint: str, params: dict, timeout: float = 10.0) -> dict:
        log = logger.bind(endpoint=endpoint, params=params)
        log.info("Requesting endpoint")
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(f"{self.BASE_URL}/{endpoint}", params=params)
            log_resp = log.bind(status_code=resp.status_code)
            log_resp.info(f"Response body={resp.text}")
            resp.raise_for_status()
            return resp.json()

    async def cek_loan(
        self, username: str, to: str, timeout: float = 10.0
    ) -> DigiposApiResponse:
        """Request ke endpoint /cek_loan OtomaX."""
        params = {"username": username, "to": to}
        data = await self._get("cek_loan", params, timeout)
        return DigiposApiResponse(**data)

    async def list_denom(
        self,
        username: str,
        to: str,
        payment_method: str,
        amount: int,
        up_harga: int = 0,
        json: int = 1,
        timeout: float = 10.0,
    ) -> dict:
        """Request ke endpoint /list_denom OtomaX."""
        params = {
            "username": username,
            "to": to,
            "payment_method": payment_method,
            "amount": amount,
            "json": json,
            "up_harga": up_harga,
        }
        return await self._get("list_denom", params, timeout)

    async def trx_pulsa(
        self,
        username: str,
        pin: str,
        payment_method: str,
        to: str,
        amount: int,
        type_: str,
        idtrx: str,
        check: int | None = None,
        timeout: float = 10.0,
    ) -> dict:
        """Request ke endpoint /pulsa."""
        params = {
            "username": username,
            "pin": pin,
            "payment_method": payment_method,
            "to": to,
            "amount": amount,
            "type": type_,
            "idtrx": idtrx,
        }
        if check is not None:
            params["check"] = check
        return await self._get("pulsa", params, timeout)
