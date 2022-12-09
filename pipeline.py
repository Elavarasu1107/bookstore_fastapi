from dagster import asset
import requests


@asset
def register():
    user_data = {
        "username": "User5",
        "password": "password",
        "email": "sellamuthuappusamy@gmail.com",
        "phone": 9087654321,
        "location": "Salem",
        "first_name": "Elavarasu",
        "last_name": "Appusamy"
    }
    response = requests.post(url="http://127.0.0.1:8000/user/register/", json=user_data,
                            headers={"Content-Type": "application/json"})
    return response.json()


@asset
def login():
    login_data = {"username": "User1",
                  "password": "password"}
    response = requests.post(url="http://127.0.0.1:8000/user/login/", json=login_data,
                             headers={"Content-Type": "application/json"})
    return response.json()


@asset
def create_book(login):
    book_data = {
        "author": "Something",
        "title": "Nothing",
        "price": 250,
        "quantity": 20
    }
    response = requests.post(url="http://127.0.0.1:8000/book/create/", json=book_data,
                             headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()
