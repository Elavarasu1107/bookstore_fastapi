import logging
from os import environ

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Response, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, Book, User
from validators import BookValidator, UserIdValidator, UserLoginValidator, UserValidator

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
