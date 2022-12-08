from fastapi import APIRouter, Depends, Request, Response, status

from event_emitter import ee
from models import Book, Cart, CartItem, CartStatus, User
from utils import logger, verify_user
from validators import CartValidator, IdValidator

router = APIRouter()


@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_cart(request: Request, response: Response, payload: CartValidator, user: User = Depends(verify_user)):
    try:
        payload.user_id = user.id
        cart = Cart.objects.get_or_none(user_id=payload.user_id, status=CartStatus.cart.value)
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


@router.get("/get/", status_code=status.HTTP_200_OK)
def get_cart(request: Request, response: Response, user: User = Depends(verify_user)):
    try:
        carts = CartItem.objects.filter(user_id=user.id)
        data = [items.to_dict() for items in carts]
        return {"message": "Cart Retrieved", "status": 200, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.put("/update/", status_code=status.HTTP_201_CREATED)
def update_cart(request: Request, response: Response, payload: CartValidator, user: User = Depends(verify_user)):
    try:
        cart = Cart.objects.get(id=payload.id, user_id=user.id, status=CartStatus.cart.value)
        book = Book.objects.get(id=payload.book_id)
        cartitem = CartItem.objects.filter(cart_id=cart.id, user_id=user.id, book_id=payload.book_id)
        count = payload.quantity - len(cartitem)
        ee.emit("update_cart", cart, user, book, cartitem, count)
        return {"message": "Cart Updated", "status": 201, "data": cart.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(request: Request, response: Response, payload: IdValidator, user: User = Depends(verify_user)):
    try:
        Cart.objects.delete(id=payload.id, user_id=user.id)
        return {"message": "Cart Deleted", "status": 204, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}
