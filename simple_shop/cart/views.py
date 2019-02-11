from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.apps import apps

from .cart import Cart
from .forms import CartAddPairForm


Pair = apps.get_model('shop', 'Pair')


@require_POST
def cart_add(request):
    cart = Cart(request)
    form = CartAddPairForm(data=request.POST)
    pair = get_object_or_404(Pair, id=request.POST['pair'])
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(pair=cd['pair'],
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return redirect('cart:cart_detail')
    messages.error(
        request, message=f"You chose to many pairs. Max available pairs of size { pair.get_available_pair } is: { pair.quantity }")
    return redirect('shop:product_detail_view', pair.product.slug)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_remove(request, pair):
    cart = Cart(request)
    cart.remove(pair)
    return redirect('cart:cart_detail')
