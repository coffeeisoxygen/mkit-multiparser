import pytest
from app.exception.base import AppExceptionError
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
