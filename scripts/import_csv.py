"""Load validated CSV files into already-created PostgreSQL tables."""
from pathlib import Path

import pandas as pd
from sqlalchemy import inspect
from db_config import get_engine

root = Path(__file__).resolve().parents[1]
data_dir = root / "data"

# Parents must be inserted before children with foreign keys.
imports = [
    ("categories", "categories.csv", ["category_id", "name"]),
    ("authors", "authors.csv", ["author_id", "full_name"]),
    ("users", "users.csv", ["user_id", "full_name", "email"]),
    ("books", "books.csv", ["book_id", "title", "isbn",
                            "publication_year", "category_id"]),
    ("book_authors", "book_authors.csv", ["book_id", "author_id"]),
]

# One transaction: all files load, or none of the inserts remain.
with get_engine().begin() as connection:
    inspector = inspect(connection)
    for table, filename, expected_columns in imports:
        if not inspector.has_table(table, schema="public"):
            raise RuntimeError(f"Table '{table}' is missing. Run create_schema.py")

        csv_path = data_dir / filename
        frame = pd.read_csv(csv_path, dtype={"isbn": "string"})
        if list(frame.columns) != expected_columns:
            raise ValueError(f"Incorrect CSV columns in {filename}")
        if frame.empty or frame.isna().any().any():
            raise ValueError(f"Empty file or missing values: {filename}")

        frame.to_sql(table, con=connection, if_exists="append",
                    index=False, method="multi")
        print(f"Imported {len(frame)} rows into {table}")

print("Import completed successfully.")