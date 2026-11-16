import requests

BASE_URL = "http://127.0.0.1:8000"
BOOK_ID = 1  # Replace with an existing book ID

def test_get_existing_book_http():
    response = requests.get(f"{BASE_URL}/books/{BOOK_ID}", timeout=5)
    assert response.status_code == 200
    assert response.json()["book_id"] == BOOK_ID