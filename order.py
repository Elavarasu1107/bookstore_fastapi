from fastapi import APIRouter, Depends, Request, Response, status

from models import Cart, User
from utils import logger, verify_user
from validators import IdValidator

router = APIRouter()

@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_order(request:Request, response: Response, payload: IdValidator, user: User=Depends(verify_user)):
    try:
        cart = Cart.objects.get_or_none(id=payload.id, user_id=user.id, status=False)
        if cart:
            cart.objects.update(id=payload.id, user_id=user.id, status=True)
            return {"message": "Order placed", "status": 201, "data": cart.to_dict()}
        return {"message": "Order already placed", "status": 201, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def create_order(request:Request, response: Response, payload: IdValidator, user: User=Depends(verify_user)):
    try:
        cart = Cart.objects.get_or_none(id=payload.id, user_id=user.id, status=True)
        if cart:
            cart.objects.delete(id=payload.id, user_id=user.id)
            return {"message": "Order cancelled", "status": 204, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}