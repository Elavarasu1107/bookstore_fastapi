from os import environ

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship

from settings import settings

Base = declarative_base()
engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)


class Manager:
    def __init__(self) -> None:
        self.model = None
        self.session = Session(engine)


    def create(self, **payload):
        instance = self.model(**payload)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def bulk_create(self, *instances):
        self.session.add_all(*instances)
        self.session.commit()

    def update(self, **payload):
        instance = self.get(id=payload.get("id"))
        for k, v in payload.items():
            setattr(instance, k, v)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, **payload):
        instance = self.get(id=payload.get("id"))
        self.session.delete(instance)
        self.session.commit()

    def get(self, **payload):
        instance = self.session.query(self.model).filter_by(**payload).one()
        return instance

    def get_or_none(self, **payload):
        instance = self.session.query(self.model).filter_by(**payload).one_or_none()
        return instance

    def filter(self, **payload):
        instance_list = self.session.query(self.model).filter_by(**payload).all()
        return instance_list

    def all(self):
        instance_list = self.session.query(self.model).all()
        return instance_list

    def __set_name__(self, owner, name):
        self.model = owner

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(250), unique=True)
    password = Column(String(250))
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(150))
    phone = Column(BigInteger)
    location = Column(String(150))
    is_superuser = Column(Boolean, default=False)
    book = relationship("Book", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    cartitem = relationship("CartItem", back_populates="user")
    order = relationship("Order", back_populates="user")
    orderitem = relationship("OrderItem", back_populates="user")
    objects = Manager()

    def __repr__(self):
        return f"User(id={self.id!r})"

    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "phone": self.phone, "location": self.location}


class Book(Base):
    __tablename__ = "book"

    id = Column(BigInteger, primary_key=True, index=True)
    author = Column(String(250))
    title = Column(String(250))
    price = Column(Integer)
    quantity = Column(Integer)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="book")
    cartitem = relationship("CartItem", back_populates="book")
    orderitem = relationship("OrderItem", back_populates="book")
    objects = Manager()

    def __repr__(self):
        return f"Book(id={self.id!r})"


    def to_dict(self):
        return {"id": self.id, "author": self.author, "title": self.title, "price": self.price,
                "quantity": self.quantity, "user": self.user_id}


class Cart(Base):
    __tablename__ = "cart"

    id = Column(BigInteger, primary_key=True, index=True)
    total_quantity = Column(Integer, default=0)
    total_price = Column(Integer, default=0)
    status = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cart")
    cartitem = relationship("CartItem", back_populates="cart", cascade="all,delete")
    order = relationship("Order", back_populates="cart")
    objects = Manager()

    def __repr__(self):
        return f"Cart(id={self.id!r})"


    def to_dict(self):
        return {"id": self.id, "total_quantity": self.total_quantity, "total_price": self.total_price, "status": self.status,
                "user_id": self.user_id}


class CartItem(Base):
    __tablename__ = "cartitem"

    id = Column(BigInteger, primary_key=True, index=True)
    price = Column(Integer)
    quantity = Column(Integer)
    book_id = Column(BigInteger, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", back_populates="cartitem")
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cartitem")
    cart_id = Column(BigInteger, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    cart = relationship("Cart", back_populates="cartitem")
    objects = Manager()

    def __repr__(self):
        return f"CartItem(id={self.id!r})"


    def to_dict(self):
        return {"id": self.id, "price": self.price, "book_id": self.book_id, "user_id": self.user_id, "cart_id": self.cart_id}


class Order(Base):
    __tablename__ = "order"

    id = Column(BigInteger, primary_key=True, index=True)
    total_quantity = Column(Integer, default=0)
    total_price = Column(Integer, default=0)
    cart_id = Column(BigInteger, ForeignKey("cart.id", ondelete="SET NULL"), nullable=True)
    cart = relationship("Cart", back_populates="order")
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="order")
    orderitem = relationship("OrderItem", back_populates="order", cascade="all,delete")
    objects = Manager()

    def __repr__(self):
        return f"Order(id={self.id!r})"

    def to_dict(self):
        return {"id": self.id, "total_quantity": self.total_quantity, "total_price": self.total_price, "cart_id": self.cart_id,
                "user_id": self.user_id}


class OrderItem(Base):
    __tablename__ = "orderitem"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="orderitem")
    book_id = Column(BigInteger, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", back_populates="orderitem")
    order_id = Column(BigInteger, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order", back_populates="orderitem")
    objects = Manager()

    def __repr__(self):
        return f"OrderItem(id={self.id!r})"

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "book_id": self.book_id, "order_id": self.order_id}
