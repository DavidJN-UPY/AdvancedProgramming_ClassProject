"""Execute the SQL file that defines tables and relationships."""
from pathlib import Path
from db_config import get_engine

root = Path(__file__).resolve().parents[1]
sql_file = root / "sql" / "01_create_tables.sql"

statement = sql_file.read_text(encoding="utf-8")

with get_engine().begin() as connection:
    connection.exec_driver_sql(statement)

print("Schema created (or existing tables found).")
