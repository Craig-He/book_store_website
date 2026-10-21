from Book import *
from database_connection import *

class BookRepository():
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        table = self.connection.execute("SELECT * FROM books")
        books = []
        for record in table:
            book = Book(record["title"], record["author"], record["id"])
            books.append(book)
        return books

    def create(self, book):
        self.connection.execute("INSERT INTO books (title, author) VALUES (%s, %s)", [book.title, book.author])