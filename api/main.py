from fastapi import FastAPI,HTTPException
from sqlalchemy import text

from scripts.db_config import get_engine

app=FastAPI(title="Book Management API")
engine= get_engine()

@app.get("/books")
def list_books():
    query=text("""
        SELECT book_id, title, isbn, publication_year
        FROM books
        ORDER BY book_id
    """)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
    return [dict(row) for row in rows]

@app.get("/books/{book_id}")
def get_book(book_id: int):
    query=text("""
        SELECT book_id, title, isbn, publication_year
        FROM books
        WHERE book_id = :book_id
    """)
    with engine.connect() as connection:
        row=connection.execute(
            query,{"book_id":book_id}
        ).mappings().first()
    if row is None:
        raise HTTPException(status_code=404,detail="Book not found")
    return dict(row)

@app.get("/categories/{category_id}/books")
def list_category_books(category_id: int):
    query=text("""
        SELECT b.book_id, b.title, c.name AS category
        FROM books AS b
        JOIN categories AS c
            ON b.category_id = c.category_id
        WHERE c.category_id = :category_id
        ORDER BY b.book_id
    """)
    with engine.connect() as connection:
        rows=connection.execute(
            query,{"category_id":category_id}
        ).mappings().all()
    return [dict(row) for row in rows]