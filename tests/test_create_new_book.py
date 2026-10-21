# in a new file called `test_create_new_book.py`

from database_connection import *
from playwright.sync_api import Page, expect

def test_create_book(page:Page):
    page.goto("http://127.0.0.1:5001/books")

    page.get_by_label("Title").fill("The Chroicles of Geronimo (the cat)")
    page.get_by_label("Author").fill("Geronimo")
    page.get_by_role("button", name="Submit").click()


    books = page.locator("li")
    newBook = books.all_inner_texts()[-1]


    assert "The Chroicles of Geronimo (the cat) by Geronimo" == newBook



