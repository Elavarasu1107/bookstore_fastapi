from pydantic import BaseModel, EmailStr


class UserIdValidator(BaseModel):
    user_id: int

class UserValidator(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    location: str
    is_superuser: bool|None= False


class UserLoginValidator(BaseModel):
    username: str
    password: str


class BookValidator(BaseModel):
    author: str
    title: str
    price: int
    quantity: int
    user_id: int


class CartValidator(BaseModel):
    user_id: int