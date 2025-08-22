import httpx
import pytest
from app.external.digipos.pulsa import DigiposApiClient

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_cek_loan(monkeypatch):
    async def mock_get(self, url, params=None, timeout=None):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "req": {"username": "user", "to": "081295221639"},
                    "res": '{"status": "ok", "data": {"loan": 1000}}',
                }

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
    client = DigiposApiClient()
    result = await client.cek_loan("user", "081295221639")
    print("DigiposApiResponse object:", result)
    print("req:", result.req)
    print("res:", result.res)
    # Parse the JSON string in result.res for assertion
    import json

    res_data = json.loads(result.res)
    assert res_data["status"] == "ok"
    assert "loan" in res_data["data"]


@pytest.mark.asyncio
async def test_list_denom(monkeypatch):
    def mock_get(self, url, params=None, timeout=None):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": "ok", "denom": [5000, 10000]}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
    client = DigiposApiClient()
    result = await client.list_denom("user", "081295221639", "LINKAJA", 5000)
    assert result["status"] == "ok"
    assert 5000 in result["denom"]


@pytest.mark.asyncio
async def test_trx_pulsa(monkeypatch):
    def mock_get(self, url, params=None, timeout=None):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"status": "success", "trxid": "12345"}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
    client = DigiposApiClient()
    result = await client.trx_pulsa(
        "user", "1234", "NGRS", "081295221639", 5000, "FIX", "trxid123"
    )
    assert result["status"] == "success"
    assert result["trxid"] == "12345"
