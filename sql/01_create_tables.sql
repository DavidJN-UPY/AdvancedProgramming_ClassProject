-- Run only after creating the book_management database.
-- Identifiers are provided by the sample CSV files.
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT chk_category_name
        CHECK (length(btrim(name)) > 0)
);
CREATE TABLE IF NOT EXISTS authors (
    author_id INTEGER PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    CONSTRAINT chk_author_name
        CHECK (length(btrim(full_name)) > 0)
);
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
email VARCHAR(254) NOT NULL UNIQUE,
CONSTRAINT chk_user_email
CHECK (position('@' IN email) > 1)
);
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) NOT NULL UNIQUE,
    publication_year SMALLINT NOT NULL,
    category_id INTEGER NOT NULL,
    CONSTRAINT fk_book_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_book_title
        CHECK (length(btrim(title)) > 0),
    CONSTRAINT chk_book_isbn
        CHECK (isbn ~ '^[0-9]{13}$'),
    CONSTRAINT chk_publication_year
        CHECK (publication_year BETWEEN 1450 AND 2100)
);
CREATE TABLE IF NOT EXISTS book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_link_book
        FOREIGN KEY (book_id)
        REFERENCES books(book_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_link_author
        FOREIGN KEY (author_id)
        REFERENCES authors(author_id) 
        ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_books_category
    ON books(category_id);
CREATE INDEX IF NOT EXISTS idx_link_author
    ON book_authors(author_id);