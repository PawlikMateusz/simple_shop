from django.conf import settings
from django.contrib import messages
from django.http import request
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.apps import apps

Pair = apps.get_model('shop', 'Pair')


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, pair, quantity=1, update_quantity=False):
        if str(pair.id) not in self.cart:
            print('new item')
            if pair.product.discount_price:
                self.cart[str(pair.id)] = {'quantity': 0,
                                           'pair': pair.id,
                                           'price': str(pair.product.discount_price)}
            else:
                self.cart[str(pair.id)] = {'quantity': 0,
                                           'pair': pair.id,
                                           'price': str(pair.product.price)}
        if update_quantity:
            if quantity > pair.quantity:
                messages.error(
                    self.request, f"We have only {pair.quantity} pair/s of this shoe number")
            else:
                self.cart[pair.id]['quantity'] = quantity
        else:
            quantity_after_sum = self.cart[str(pair.id)]['quantity'] + quantity
            if quantity_after_sum > pair.quantity:
                messages.error(
                    self.request, f"We have only {pair.quantity} pair/s of this shoe number")
            else:
                self.cart[str(pair.id)]['quantity'] = quantity_after_sum
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, pair):
        if pair in self.cart:
            del self.cart[pair]
            self.save()

    def __iter__(self):
        for item in self.cart.values():
            pair = get_object_or_404(Pair, id=item['pair'])
            item['pair'] = pair
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
