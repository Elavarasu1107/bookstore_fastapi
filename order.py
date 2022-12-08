from fastapi import APIRouter, Depends, Request, Response, status

from models import Book, Cart, CartItem, CartStatus, User
from utils import logger, verify_user
from validators import IdValidator, OrderOutput

router = APIRouter()


@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_order(request: Request, response: Response, payload: IdValidator, user: User = Depends(verify_user)):
    try:
        cart = Cart.objects.get_or_none(id=payload.id, user_id=user.id, status=CartStatus.cart.value)
        if cart:
            cart.objects.update(id=payload.id, user_id=user.id, status=CartStatus.ordered.value)
            return {"message": "Order placed", "status": 201, "data": cart.to_dict()}
        return {"message": "Order already placed", "status": 201, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.get("/get/", status_code=status.HTTP_200_OK)
def create_order(request: Request, response: Response, user: User = Depends(verify_user)):
    try:
        data = []
        carts = Cart.objects.filter(user_id=user.id, status=CartStatus.ordered.value)
        for cart in carts:
            cart_items = CartItem.objects.filter(user_id=user.id, cart_id=cart.id)
            book_list = []
            for item in cart_items:
                book = Book.objects.get(id=item.book_id).title
                if book not in book_list:
                    book_list.append(book)
            data.append({"total_quantity": cart.total_quantity, "total_price": cart.total_price, "book": book_list})
        return {"message": "Order Retrieved", "status": 201, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.delete("/delete/", status_code=status.HTTP_205_RESET_CONTENT)
def create_order(request: Request, response: Response, payload: IdValidator, user: User = Depends(verify_user)):
    try:
        cart = Cart.objects.get_or_none(id=payload.id, user_id=user.id, status=CartStatus.ordered.value)
        if cart:
            cart.objects.update(id=payload.id, user_id=user.id, status=CartStatus.cancelled.value)
            return {"message": "Order cancelled", "status": 205, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}
