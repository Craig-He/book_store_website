from flask import Flask, render_template, request, redirect, session

from Book import Book
from BookRepository import BookRepository

from User import *
from UserRepository import UserRepository

from database_connection import DatabaseConnection
from login_required import *

app = Flask(__name__)
app.secret_key = "some_really_secret_key"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/team", methods=["GET"])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team = team)



@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"


@app.route('/books', methods=['GET'])
@login_required
def books():
    
    connection = DatabaseConnection()
    connection.connect()
    book_repo = BookRepository(connection)
    books = book_repo.all()
    print(books)
    return render_template("books.html", books= books)


@app.route('/books', methods=['POST'])
def create_book():
    
    connection = DatabaseConnection()
    connection.connect()
    
    book_details = request.form
    
    book_repo = BookRepository(connection)

    book = Book(title=book_details["title"], author=book_details["author"])
    book_repo.create(book)
    books = book_repo.all()  
    
    return redirect("/books")

@app.route('/users/new', methods=['GET'])
def get_signup_form():
    return render_template("signup_form.html")

@app.route('/users', methods=['POST'])
def create_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)
    user_details = request.form
    user = User(username=user_details["username"], password=user_details["password"])
    user_repository.create(user)
    return redirect("/books")

@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template("login_form.html")

@app.route('/sessions', methods=['POST'])
def create_session():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    user = user_repository.find_by_username(username)
    if user and user.password == password:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/books")
    else:
        return redirect("/sessions/new")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5001, debug= True)
