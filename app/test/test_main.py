from fastapi import status


def test_health_check(test_client):
    response = test_client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
