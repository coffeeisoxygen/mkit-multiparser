import pytest
from app.exception.base import AppExceptionError
from app.exception.exceptions import IPBlockedError, RequestValidationError
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("path", ["/raise"])
def test_exception_handler(app_with_exception, path):
    @app_with_exception.get(path)
    def raise_error():
        raise AppExceptionError(message="Test error")

    client = TestClient(app_with_exception)
    response = client.get(path)
    assert response.status_code == 500


def test_exception_handler_custom_status(app_with_exception):
    @app_with_exception.get("/blocked")
    def blocked():
        raise IPBlockedError(ip="1.2.3.4", endpoint="/blocked")

    client = TestClient(app_with_exception)
    response = client.get("/blocked")
    assert response.status_code == 403
    data = response.json()
    assert data["context"]["ip"] == "1.2.3.4"
    assert data["context"]["endpoint"] == "/blocked"


def test_exception_handler_validation_error(app_with_exception):
    @app_with_exception.get("/validate")
    def validate():
        raise RequestValidationError()

    client = TestClient(app_with_exception)
    response = client.get("/validate")
    assert response.status_code == 422
    data = response.json()
    assert "validation" in data["message"].lower()


def test_exception_handler_with_cause(app_with_exception):
    @app_with_exception.get("/cause")
    def cause():
        try:
            raise ValueError("fail")  # noqa: TRY301
        except ValueError as e:
            # Use exception chaining for better traceback
            raise AppExceptionError(message="Has cause") from e

    client = TestClient(app_with_exception)
    response = client.get("/cause")
    assert response.status_code == 500
    data = response.json()
    assert "fail" in data["cause"]


def test_normal_endpoint_no_exception(app_with_exception):
    @app_with_exception.get("/ok")
    def ok():
        return {"result": "ok"}

    client = TestClient(app_with_exception)
    response = client.get("/ok")
    assert response.status_code == 200
    assert response.json()["result"] == "ok"
