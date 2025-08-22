import pytest
from app.external.digipos.pulsa import DigiposApiClient
from tests.conftest import DIGIPOS_PAYMENT_METHOD, DIGIPOS_VALID_NUMBER

pytestmark = [pytest.mark.api, pytest.mark.digipos]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_list_denom_unit(monkeypatch):
    """Unit test: mock response, verify field and up_harga calculation."""
    sample_response = {
        "status": 0,
        "message": "ok",
        "data": {
            "rechargeDenomList": [
                {
                    "denom_type": "BULK",
                    "business_model": "1",
                    "fee": 519,
                    "start_value": "5000",
                    "end_value": None,
                    "tariff_mode": None,
                    "transfer_fee_mode": "4",
                    "ad_reseller": "221304",
                    "reseller_group_id": None,
                    "total_price": 5619,
                }
            ]
        },
    }

    async def mock_get(self, endpoint, params, timeout=10.0):
        return sample_response

    monkeypatch.setattr(DigiposApiClient, "_get", mock_get)
    client = DigiposApiClient()
    up_harga = 100
    result = await client.list_denom(
        username=test_settings.DGP.username,
        to=DIGIPOS_VALID_NUMBER,
        payment_method=DIGIPOS_PAYMENT_METHOD,
        amount=5000,
        up_harga=up_harga,
        json=1,
    )
    assert result["status"] == 0
    denom = result["data"]["rechargeDenomList"][0]
    for field in ["denom_type", "fee", "start_value", "total_price"]:
        assert field in denom
    fee = denom["fee"]
    start_value = int(denom["start_value"])
    total_price = denom["total_price"]
    assert total_price - (fee + start_value) == up_harga


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_denom_integration(test_settings):
    """Integration test: actual API call, verify field and up_harga calculation."""
    client = DigiposApiClient()
    username = test_settings.DGP.username
    to = DIGIPOS_VALID_NUMBER
    payment_method = DIGIPOS_PAYMENT_METHOD
    amount = 5000
    up_harga = 100
    result = await client.list_denom(
        username=username,
        to=to,
        payment_method=payment_method,
        amount=amount,
        up_harga=up_harga,
        json=1,
    )
    assert result["status"] == 0
    assert result["message"] == "ok"
    assert "data" in result
    denom_list = result["data"].get("rechargeDenomList", [])
    assert denom_list, "rechargeDenomList should not be empty"
    denom = denom_list[0]
    for field in ["denom_type", "fee", "start_value", "total_price"]:
        assert field in denom
    fee = denom["fee"]
    start_value = int(denom["start_value"])
    total_price = denom["total_price"]
    assert total_price - (fee + start_value) == up_harga


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.negative
async def test_list_denom_wrong_payment_method(test_settings):
    """Integration test: payment_method salah, harus error format."""
    client = DigiposApiClient()
    username = test_settings.DGP.username
    to = DIGIPOS_VALID_NUMBER
    payment_method = "test"  # payment method salah
    amount = 5000
    up_harga = 100
    result = await client.list_denom(
        username=username,
        to=to,
        payment_method=payment_method,
        amount=amount,
        up_harga=up_harga,
        json=1,
    )
    assert "data" not in result
    assert "messageInfo" in result
    assert result["status"] != 0
