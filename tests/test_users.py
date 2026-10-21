from playwright.sync_api import Page, expect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_connection import DatabaseConnection
from app import app


def test_create_user_is_saved_to_database():
    client = app.test_client()

    # set up a DB connection
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    
   # send the request
    response = client.post('/users', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # assert that the redirect happened
    assert response.status_code == 302

    # read from the DB
    result = connection.execute("SELECT * FROM users WHERE username = 'testuser'")

    # assert that the user was created
    assert len(result) == 1
    assert result[0]['username'] == 'testuser'