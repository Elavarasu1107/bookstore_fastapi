import logging
from os import environ

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Response, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, Book, Cart, CartItem, User
from utils import JWT, TokenRole
from validators import (
    BookValidator,
    CartValidator,
    UserIdValidator,
    UserLoginValidator,
    UserValidator,
)

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()
load_dotenv()
app = FastAPI()
engine = create_engine(environ.get('DATABASE_URL'))
Base.metadata.create_all(engine)


@app.post("/user/register/", status_code=status.HTTP_201_CREATED)
def user_register(payload: UserValidator, response: Response):
    """
    This function registers user to the database
    """
    try:
        with Session(engine) as session:
            user = User(**payload.dict())
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"message": "User Registered", "status": 201, "data": user.to_dict()}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}

@app.post('/user/login/', status_code=status.HTTP_202_ACCEPTED)
def user_login(payload: UserLoginValidator, response: Response):
    try:
        session = Session(engine)
        query = select(User).where(User.username == payload.username).where(User.password == payload.password)
        users = session.scalars(query).all()
        if len(users) == 1:
            token = JWT().encode({"user_id": users[0].id, "role": TokenRole.auth.value})
            return {"message": "Login Successful", "status": 202, "data": token}
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": "Invalid Credentials", "status": 406, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.post('/note/create/', status_code=status.HTTP_201_CREATED)
def create_note(payload: BookValidator, response: Response):
    try:
        session = Session(engine)
        query = select(User).where(User.id==payload.user_id)
        users = session.scalars(query).all()
        if len(users) == 1:
            if users[0].is_superuser == True:
                with Session(engine) as session:
                    book = Book(**payload.dict())
                    session.add(book)
                    session.commit()
                    session.refresh(book)
                    return {"message": "Book Added", "status": 201, "data": book.to_dict()}
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "User not Authorized", "status": 401, "data": {}}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found", "status": 404, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.get('/note/get/', status_code=status.HTTP_200_OK)
def get_note(request: Request, response: Response):
    try:
        session = Session(engine)
        query = select(Book)
        books = session.scalars(query).all()
        data = [book.to_dict() for book in books]
        return {"message": "Books Retrieved", "status": 200, "data": data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.put('/note/update/{book_id}', status_code=status.HTTP_201_CREATED)
def update_note(book_id: int, payload: BookValidator, response: Response):
    try:
        session = Session(engine)
        query = select(User).where(User.id==payload.user_id)
        users = session.scalars(query).all()
        if len(users) == 1:
            if users[0].is_superuser == True:
                with Session(engine) as session:
                    query = select(Book).where(Book.id == book_id)
                    book = session.scalars(query).one()
                    book.author = payload.author
                    book.title = payload.title
                    book.price = payload.price
                    book.quantity = payload.quantity
                    session.commit()
                    session.refresh(book)
                    return {"message": "Book Updated", "status": 201, "data": book.to_dict()}
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "User not Authorized", "status": 401, "data": {}}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found", "status": 404, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@app.delete('/note/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(book_id: int, payload: UserIdValidator, response: Response):
    try:
        session = Session(engine)
        query = select(User).where(User.id==payload.user_id)
        users = session.scalars(query).all()
        if len(users) == 1:
            if users[0].is_superuser == True:
                with Session(engine) as session:
                    query = select(Book).where(Book.id == book_id)
                    book = session.scalars(query).one()
                    session.delete(book)
                    session.commit()
                    return {"message": "Book Deleted", "status": 204, "data":{}}
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "User not Authorized", "status": 401, "data": {}}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found", "status": 404, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}
