from fastapi.testclient import TestClient
from api.main import app

BOOK_ID = 1  # Use the same existing book ID

def test_get_existing_book_client():
    with TestClient(app) as client:
        response = client.get(f"/books/{BOOK_ID}")
    assert response.status_code == 200
    assert response.json()["book_id"] == BOOK_ID