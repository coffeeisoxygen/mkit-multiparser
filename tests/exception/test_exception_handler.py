from fastapi.testclient import TestClient


def test_exception_handler(app_with_exception):
    @app_with_exception.get("/raise")
    def raise_error():
        from app.exception.base import AppExceptionError

        raise AppExceptionError(message="Test error")

    client = TestClient(app_with_exception)
    response = client.get("/raise")
    assert response.status_code == 500
