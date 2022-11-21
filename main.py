from typing import Any

from fastapi import Depends, FastAPI, Request, Response, status

from event_emitter import ee
from models import Book, Cart, CartItem, Order, OrderItem, User
from utils import JWT, TokenRole, logger, verify_superuser, verify_user
from validators import (
    BookValidator,
    CartIdValidator,
    CartValidator,
    IdValidator,
    OrderItemOutput,
    UserLoginValidator,
    UserValidator,
)

app = FastAPI()

@app.post("/user/register/", status_code=status.HTTP_201_CREATED)
def user_register(payload: UserValidator, response: Response):
    """
    This function registers user to the database
    """
    try:
        user = User.objects.create(**payload.dict())
        return {"message": "User Registered", "status": 201, "data": user.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}

@app.post('/user/login/', status_code=status.HTTP_202_ACCEPTED)
def user_login(payload: UserLoginValidator, response: Response):
    try:
        user = User.objects.get_or_none(**payload.dict())
        if user:
            token = JWT().encode({"user_id": user.id, "role": TokenRole.auth.value})
            return {"message": "Login Successful", "status": 202, "data": token}
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": "Invalid Credentials", "status": 406, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.post('/book/create/', status_code=status.HTTP_201_CREATED)
def create_note(payload: BookValidator, response: Response, user: User=Depends(verify_superuser)):
    try:
        payload.user_id = user.id
        book = Book.objects.create(**payload.dict())
        return {"message": "Book Added", "status": 201, "data": book.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.get('/book/get/', status_code=status.HTTP_200_OK)
def get_note(request: Request, response: Response, user: User=Depends(verify_user)):
    try:
        books = Book.objects.all()
        data = [book.to_dict() for book in books]
        return {"message": "Books Retrieved", "status": 200, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.put('/book/update/', status_code=status.HTTP_201_CREATED)
def update_note(payload: BookValidator, response: Response, user: User=Depends(verify_superuser)):
    try:
        payload.user_id = user.id
        book = Book.objects.update(**payload.dict())
        return {"message": "Book Updated", "status": 201, "data": book.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.delete('/book/delete/', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(payload: IdValidator, response: Response, user: User=Depends(verify_superuser)):
    try:
        payload.id = user.id
        Book.objects.delete(**payload.dict())
        return {"message": "Book Deleted", "status": 204, "data":{}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.post("/cart/create/", status_code=status.HTTP_201_CREATED)
def create_cart(request: Request, response: Response, payload: CartValidator, user: User=Depends(verify_user)):
    try:
        payload.user_id = user.id
        cart = Cart.objects.get_or_none(user_id=payload.user_id, status=False)
        book = Book.objects.get(id=payload.book_id)
        if not cart:
            cart = Cart.objects.create(user_id=payload.user_id)
            ee.emit("add_cart", payload, user, book, cart)
            return {"message": "Cart created", "status": 201, "data": cart.to_dict()}
        ee.emit("add_cart", payload, user, book, cart)
        return {"message": "Cart created", "status": 201, "data": cart.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.get("/cart/get/", status_code=status.HTTP_200_OK)
def get_cart(request:Request, response: Response, user: User=Depends(verify_user)):
    try:
        carts = CartItem.objects.filter(user_id=user.id)
        data = [items.to_dict() for items in carts]
        return {"message": "Cart Retrieved", "status": 200, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.put("/cart/update/", status_code=status.HTTP_201_CREATED)
def update_cart(request:Request, response: Response, payload: CartValidator, user: User=Depends(verify_user)):
    try:
        cart = Cart.objects.get(id=payload.id, user_id=user.id, status=False)
        book = Book.objects.get(id=payload.book_id)
        cartitem = CartItem.objects.filter(cart_id=cart.id, user_id=user.id, book_id=payload.book_id)
        count = payload.quantity - len(cartitem)
        ee.emit("update_cart", cart, user, book, cartitem, count)
        return {"message": "Cart Updated", "status": 201, "data": cart.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.delete("/cart/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(request:Request, response: Response, payload: CartIdValidator, user: User=Depends(verify_user)):
    try:
        Cart.objects.delete(id=payload.id, user_id=user.id)
        return {"message": "Cart Deleted", "status": 204, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}

@app.post("/order/create/", status_code=status.HTTP_201_CREATED)
def create_order(request:Request, response: Response, payload: CartIdValidator, user: User=Depends(verify_user)):
    try:
        cart = Cart.objects.get_or_none(id=payload.id, user_id=user.id, status=False)
        if cart:
            books = CartItem.objects.filter(cart_id=cart.id, user_id=user.id)
            book_list = []
            for book in books:
                book_list.append(book.book_id)
            order = Order.objects.create(cart_id=cart.id, user_id=user.id)
            data = {"book_list": book_list, "order_id": order.id, "quantity": len(book_list), "user_id": user.id}
            ee.emit("add_order", data)
            order.objects.update(id=order.id, total_quantity=cart.total_quantity, total_price=cart.total_price)
            cart.objects.update(id=cart.id, status=True)
            return {"message": "Order placed", "status": 201, "data": order.to_dict()}
        return {"message": "Order already placed", "status": 201, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}
    
@app.get("/order/get/", status_code=status.HTTP_200_OK, response_model=list[OrderItemOutput]|dict[str,Any])
def create_order(request:Request, response: Response, user: User=Depends(verify_user)):
    try:
        order = Order.objects.get_or_none(user_id=user.id)
        orderitems = OrderItem.objects.filter(user_id=user.id, order_id=order.id)
        return orderitems
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}

@app.delete("/order/delete/", status_code=status.HTTP_204_NO_CONTENT)
def create_order(request:Request, response: Response, payload: IdValidator, user: User=Depends(verify_user)):
    try:
        Order.objects.delete(id=payload.id, user_id=user.id)
        return {"message": "Order cancelled", "status": 204, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}