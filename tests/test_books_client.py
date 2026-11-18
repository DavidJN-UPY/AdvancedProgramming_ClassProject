"""Method B: automated API tests with FastAPI TestClient (no Uvicorn needed)."""

from fastapi.testclient import TestClient
from api.main import app

# Known test records (same data used in test_books_http.py)
BOOK_ID = 1
KNOWN_BOOK = {
    "book_id": 1,
    "title": "Dune",
    "isbn": "9780441172719",
    "publication_year": 1965,
}
BOOK_FIELDS = {"book_id", "title", "isbn", "publication_year"}
CATEGORY_ID = 1
CATEGORY_NAME = "Science Fiction"
CATEGORY_BOOK_IDS = [1, 2, 3]
MISSING_CATEGORY_ID = 9999
INVALID_CATEGORY_ID = "abc"


def get(path):
    with TestClient(app) as client:
        return client.get(path)


# ---------- R-02  GET /books/{book_id}  (guided test) ----------

def test_get_existing_book_client():
    with TestClient(app) as client:
        response = client.get(f"/books/{BOOK_ID}")
    assert response.status_code == 200
    assert response.json()["book_id"] == BOOK_ID


# ---------- R-01  GET /books ----------

def test_list_books_returns_records_client():
    """R-01.1: the collection is available and contains records."""
    response = get("/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) > 0


def test_list_books_structure_client():
    """R-01.2: every record matches the API contract."""
    response = get("/books")
    assert response.status_code == 200
    for book in response.json():
        assert set(book.keys()) == BOOK_FIELDS
        assert isinstance(book["book_id"], int)
        assert isinstance(book["title"], str) and book["title"]
        assert isinstance(book["isbn"], str)
        assert isinstance(book["publication_year"], int)


def test_list_books_known_data_client():
    """R-01.3: returned records match known data and are ordered by ID."""
    response = get("/books")
    assert response.status_code == 200
    books = response.json()
    assert KNOWN_BOOK in books
    ids = [book["book_id"] for book in books]
    assert ids == sorted(ids)


# ---------- R-03  GET /categories/{category_id}/books ----------

def test_category_with_books_client():
    """R-03.1: an existing category returns its books."""
    response = get(f"/categories/{CATEGORY_ID}/books")
    assert response.status_code == 200
    books = response.json()
    assert [book["book_id"] for book in books] == CATEGORY_BOOK_IDS
    assert all(book["category"] == CATEGORY_NAME for book in books)


def test_category_not_found_client():
    """R-03.2: a category ID that does not exist returns an empty list."""
    response = get(f"/categories/{MISSING_CATEGORY_ID}/books")
    assert response.status_code == 200
    assert response.json() == []


def test_category_invalid_id_client():
    """R-03.3: a non-integer category ID is rejected with HTTP 422."""
    response = get(f"/categories/{INVALID_CATEGORY_ID}/books")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "category_id"]
