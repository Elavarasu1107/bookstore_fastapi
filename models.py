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

    def __repr__(self):
        return f"User(id={self.id!r})"

    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "first_name": self.first_name, "last_name": self.last_name,
        "email": self.email, "phone": self.phone, "location": self.location}


# class Book(Base):
#     __tablename__ = "book"

#     id = Column(BigInteger, primary_key=True, index=True)
#     author = Column(String(250))
#     title = Column(String(250))
#     price = Column(String(250))
#     quantity = Column(String(250))
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#     user = relationship("User", back_populates="book")
