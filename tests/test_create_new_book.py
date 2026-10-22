from playwright.sync_api import Page, expect
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_connection import DatabaseConnection

def test_create_book(page:Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234')")


    page.goto("http://localhost:5001/sessions/new")
    page.get_by_label("username").fill("test")
    page.get_by_label("password").fill("1234")
    page.get_by_role("button").click()

    page.goto("http://localhost:5001/books")
    page.get_by_label("Title").fill("The Chroicles of Geronimo (the cat)")
    page.get_by_label("Author").fill("Geronimo")
    page.get_by_role("button", name="Submit").click()


    books = page.locator("li")
    newBook = books.all_inner_texts()[-1]


    assert "The Chroicles of Geronimo (the cat) by Geronimo" == newBook



