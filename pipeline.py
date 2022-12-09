from dagster import asset
import requests


@asset(config_schema={"username": str, "password": str, "email": str, "phone": int, "location": str, "first_name": str,
                      "last_name": str})
def register(context):
    user_data = {
        "username": context.op_config.get("username"),
        "password": context.op_config.get("password"),
        "email": context.op_config.get("email"),
        "phone": context.op_config.get("phone"),
        "location": context.op_config.get("location"),
        "first_name": context.op_config.get("first_name"),
        "last_name": context.op_config.get("last_name")
    }
    response = requests.post(url="http://127.0.0.1:8000/user/register/", json=user_data,
                             headers={"Content-Type": "application/json"})
    return response.json()


@asset(config_schema={"username": str, "password": str})
def login(context):
    login_data = {"username": context.op_config.get("username"),
                  "password": context.op_config.get("password")}
    response = requests.post(url="http://127.0.0.1:8000/user/login/", json=login_data,
                             headers={"Content-Type": "application/json"})
    return response.json()


@asset(config_schema={"author": str, "title": str, "price": int, "quantity": int})
def create_book(context, login):
    book_data = {
        "author": context.op_config.get("author"),
        "title": context.op_config.get("title"),
        "price": context.op_config.get("price"),
        "quantity": context.op_config.get("quantity")
    }
    response = requests.post(url="http://127.0.0.1:8000/book/create/", json=book_data,
                             headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset
def get_book(login):
    response = requests.get(url="http://127.0.0.1:8000/book/get/",
                            headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset(config_schema={"id": int, "author": str, "title": str, "price": int, "quantity": int})
def update_book(context, login):
    book_data = {
        "id": context.op_config.get("id"),
        "author": context.op_config.get("author"),
        "title": context.op_config.get("title"),
        "price": context.op_config.get("price"),
        "quantity": context.op_config.get("quantity")
    }
    response = requests.put(url="http://127.0.0.1:8000/book/update/", json=book_data,
                            headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset(config_schema={"id": int})
def delete_book(context, login):
    book_id = {"id": context.op_config.get("id")}
    response = requests.delete(url="http://127.0.0.1:8000/book/delete/", json=book_id,
                               headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.status_code


@asset(config_schema={"quantity": int, "book_id": int})
def create_cart(context, login):
    cart_data = {"quantity": context.op_config.get("quantity"),
                 "book_id": context.op_config.get("book_id")}
    response = requests.post(url="http://127.0.0.1:8000/cart/create/", json=cart_data,
                             headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset
def get_cart(login):
    response = requests.get(url="http://127.0.0.1:8000/cart/get/",
                            headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset(config_schema={"id": int, "book_id": int, "quantity": int})
def update_cart(context, login):
    cart_data = {"id": context.op_config.get("id"),
                 "quantity": context.op_config.get("quantity"),
                 "book_id": context.op_config.get("book_id")}
    response = requests.put(url="http://127.0.0.1:8000/cart/update/", json=cart_data,
                            headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset(config_schema={"id": int})
def delete_cart(context, login):
    cart_id = {"id": context.op_config.get("id")}
    response = requests.delete(url="http://127.0.0.1:8000/cart/delete/", json=cart_id,
                               headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.status_code


@asset(config_schema={"id": int})
def add_order(context, login):
    cart_id = {"id": context.op_config.get("id")}
    response = requests.post(url="http://127.0.0.1:8000/order/create/", json=cart_id,
                             headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset
def get_order(login):
    response = requests.get(url="http://127.0.0.1:8000/order/get/",
                            headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.json()


@asset(config_schema={"id": int})
def delete_order(context, login):
    cart_id = {"id": context.op_config.get("id")}
    response = requests.delete(url="http://127.0.0.1:8000/order/delete/", json=cart_id,
                               headers={"Content-Type": "application/json", "token": login.get("data")})
    return response.status_code
