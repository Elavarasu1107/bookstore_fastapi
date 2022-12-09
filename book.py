from fastapi import APIRouter, Depends, Request, Response, status

from models import Book, User
from utils import logger, verify_superuser, verify_user
from validators import BookValidator, IdValidator

router = APIRouter()


@router.post('/create/', status_code=status.HTTP_201_CREATED)
def create_book(payload: BookValidator, response: Response, user: User = Depends(verify_superuser)) -> dict:
    try:
        payload.user_id = user.id
        book = Book.objects.create(**payload.dict())
        return {"message": "Book Added", "status": 201, "data": book.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.get('/get/', status_code=status.HTTP_200_OK)
def get_book(request: Request, response: Response, user: User = Depends(verify_user)) -> dict:
    try:
        books = Book.objects.all()
        data = [book.to_dict() for book in books]
        return {"message": "Books Retrieved", "status": 200, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.put('/update/', status_code=status.HTTP_201_CREATED)
def update_book(payload: BookValidator, response: Response, user: User = Depends(verify_superuser)) -> dict:
    try:
        payload.user_id = user.id
        book = Book.objects.update(**payload.dict())
        return {"message": "Book Updated", "status": 201, "data": book.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.delete('/delete/', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(payload: IdValidator, response: Response, user: User = Depends(verify_superuser)) -> dict:
    try:
        payload.user_id = user.id
        Book.objects.delete(**payload.dict())
        return {"message": "Book Deleted", "status": 204, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}
