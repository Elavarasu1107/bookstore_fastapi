from pydantic import BaseModel, EmailStr


class IdValidator(BaseModel):
    id: int

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
    id: int
    author: str
    title: str
    price: int
    quantity: int
    user_id: int|None


class CartValidator(BaseModel):
    id: int|None
    user_id: int|None
    book_id: int
    quantity: int

class CartIdValidator(BaseModel):
    id: int