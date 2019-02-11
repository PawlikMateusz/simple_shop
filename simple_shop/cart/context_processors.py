from .cart import Cart


def cart_info(request):
    cart = Cart(request)
    products_in_card = len(cart)
    cart_total_price = cart.get_total_price
    return {"cart_len": products_in_card,
            "total_price": cart_total_price}
