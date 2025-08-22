import httpx
import pytest
from app.external.digipos.pulsa import DigiposApiClient

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_checkloan_plaintext(monkeypatch):
    async def mock_get(self, url, params=None, timeout=None):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "req": {"username": "user", "to": "081295221639"},
                    "res": "Silahkan upgrade paket_terbaik",
                }

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
    client = DigiposApiClient()
    result = await client.cek_loan("user", "081295221639")
    assert result.req == {"username": "user", "to": "081295221639"}
    assert result.res == "Silahkan upgrade paket_terbaik"
