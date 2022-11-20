import logging

from pyee.base import EventEmitter

from models import Book, Cart, CartItem, User

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

ee = EventEmitter()

@ee.on('error')
def errors(ex):
    logger.exception(ex)

@ee.on("add_cart")
def add_cart(payload, user, book, cart):
    try:
        cartitem_list = []
        for i in range(payload.quantity):
            cartitem_list.append(CartItem(price=book.price, quantity=1, book_id=book.id, user_id=user.id, cart_id=cart.id))
            cart.total_price += book.price
        CartItem.objects.bulk_create(cartitem_list)
        cart.total_quantity += payload.quantity
        Cart.objects.update(id=cart.id, total_price=cart.total_price, total_quantity=cart.total_quantity)
    except Exception as ex:
        ee.emit('error', ex)

@ee.on("update_cart")
def update_cart(cart, user, book, cart_item, count):
    try:
        price = 0
        if count > 0:
            for i in range(count):
                CartItem.objects.create(price=book.price, quantity=1, book_id=book.id, user_id=user.id, cart_id=cart.id)
                price += book.price
            total_price = cart.total_price + price
            total_quantity = cart.total_quantity + count
            cart.objects.update(total_price=total_price, total_quantity=total_quantity)
        if count < 0:
            for i in range(abs(count)):
                cart_item[i].objects.delete(id=cart_item[i].id, cart_id=cart.id, user_id=user.id, book_id=book.id)
                # cart_item[i].objects.delete()
            total_price = 0
            item_list = CartItem.objects.filter(cart_id=cart.id, user_id=user.id)
            for item in item_list:
                total_price += item.price
            total_quantity = cart.total_quantity + count
            cart.objects.update(total_price=total_price, total_quantity=total_quantity)
    except Exception as ex:
        ee.emit('error', ex)