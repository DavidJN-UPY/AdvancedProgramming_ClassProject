"""A small Streamlit interface for the existing Book Management API."""

import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"


def fetch_data(path):
    """Return (JSON data, error message) from a FastAPI GET endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI. Is the server running?"
    except requests.exceptions.Timeout:
        return None, "The API took too long to respond."
    except requests.exceptions.HTTPError as error:
        status = (
            error.response.status_code
            if error.response is not None
            else "unknown"
        )
        if status == 404:
            return None, "No matching record was found (HTTP 404)."
        return None, f"The API returned HTTP {status}."
    except requests.exceptions.JSONDecodeError:
        return None, "The API did not return valid JSON."
    except requests.exceptions.RequestException:
        return None, "The request could not be completed."


def display_books(data):
    """Show a list of books from a JSON array or a 'books' wrapper."""
    if isinstance(data, list):
        books = data
    elif isinstance(data, dict):
        books = data.get("books")
    else:
        books = None

    if not isinstance(books, list):
        st.warning("Unexpected response format. Check the API output.")
        st.json(data)
    elif not books:
        st.info("No books were found.")
    else:
        st.dataframe(books, hide_index=True)


def display_book(data):
    """Show known book attributes and retain the original JSON."""
    if isinstance(data, dict) and isinstance(data.get("book"), dict):
        data = data["book"]

    if not isinstance(data, dict):
        st.warning("Unexpected response format. Check the API output.")
        st.json(data)
        return

    st.subheader(str(data.get("title", "Book details")))
    st.write(f"**Book ID:** {data.get('book_id', 'Not available')}")
    st.write(f"**ISBN:** {data.get('isbn', 'Not available')}")
    st.write(
        f"**Publication year:** "
        f"{data.get('publication_year', 'Not available')}"
    )
    with st.expander("Full API response"):
        st.json(data)


st.set_page_config(page_title="Book Management", layout="wide")
st.title("Book Management")
st.caption(
    "A simple interface connected to the existing FastAPI service."
)

all_books_tab, find_book_tab, category_tab = st.tabs(
    ["All Books", "Find Book", "By Category"]
)

with all_books_tab:
    st.subheader("Book catalog")
    if st.button("Load books"):
        data, error = fetch_data("/books")
        if error:
            st.error(error)
        else:
            display_books(data)

with find_book_tab:
    st.subheader("Find a book by ID")
    with st.form("find_book_form"):
        book_id = st.number_input("Book ID", min_value=1, step=1)
        find_submitted = st.form_submit_button("Find book")

    if find_submitted:
        data, error = fetch_data(f"/books/{book_id}")
        if error:
            st.error(error)
        else:
            display_book(data)

with category_tab:
    st.subheader("Books by category")
    with st.form("category_form"):
        category_id = st.number_input("Category ID", min_value=1, step=1)
        category_submitted = st.form_submit_button("Show books")

    if category_submitted:
        data, error = fetch_data(
            f"/categories/{category_id}/books"
        )
        if error:
            st.error(error)
        else:
            display_books(data)
