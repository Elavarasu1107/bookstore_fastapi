from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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
    cartitem = relationship("CartItem", back_populates="cart")

    def __repr__(self):
        return f"Book(id={self.id!r})"


    def to_dict(self):
        return {"id": self.id, "total_quantity": self.total_quantity, "total_price": self.total_price, "status": self.status,
                "user_id": self.user_id}


class CartItem(Base):
    __tablename__ = "cartitem"

    id = Column(BigInteger, primary_key=True, index=True)
    price = Column(Integer)
    book_id = Column(BigInteger, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", back_populates="cartitem")
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cartitem")
    cart_id = Column(BigInteger, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    cart = relationship("Cart", back_populates="cartitem")

    def __repr__(self):
        return f"Book(id={self.id!r})"


    def to_dict(self):
        return {"id": self.id, "price": self.price, "book_id": self.book_id, "user_id": self.user_id, "cart_id": self.cart_id}

