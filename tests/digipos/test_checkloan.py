import httpx
import pytest
from app.config import get_settings
from app.external.digipos.pulsa import DigiposApiClient

pytestmark = [pytest.mark.unit, pytest.mark.digipos]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_checkloan_plaintext(monkeypatch):
    async def mock_get(self, url, params=None, timeout=None):  # noqa: ARG001, RUF029
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "req": {"username": "user", "to": "081295221639"},
                    "res": "Silahkan upgrade paket_terbaik",
                }

            @property
            def text(self):
                # Simulate the response body as a string
                return '{"req": {"username": "user", "to": "081295221639"}, "res": "Silahkan upgrade paket_terbaik"}'

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
    client = DigiposApiClient()
    result = await client.cek_loan("user", "081295221639")
    assert result.req == {"username": "user", "to": "081295221639"}
    assert result.res == "Silahkan upgrade paket_terbaik"


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.asyncio
async def test_checkloan_actual():
    settings = get_settings()
    client = DigiposApiClient()
    result = await client.cek_loan(settings.DGP.username, "085352850771")
    # Output log for manual inspection
    print("Actual DigiposApiResponse:", result)
    assert isinstance(result.req, dict)
    assert isinstance(result.res, str)
