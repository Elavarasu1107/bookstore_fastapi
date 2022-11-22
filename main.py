from fastapi import FastAPI

import book
import cart
import order
import user

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(book.router, prefix="/book")
app.include_router(cart.router, prefix="/cart")
app.include_router(order.router, prefix="/order")
