from django.shortcuts import render
from django.urls import reverse_lazy
from formtools.preview import FormPreview
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView
# Create your views here.
from simple_shop.cart.cart import Cart

from django.apps import apps

Order = apps.get_model('orders', 'Order')
OrderProducts = apps.get_model('orders', 'OrderProducts')


class OrderFormPreview(FormPreview):
    preview_template = 'orders/form_preview.html'
    form_template = 'orders/form.html'

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        order = Order(user=request.user,
                      first_name=cleaned_data['first_name'],
                      last_name=cleaned_data['last_name'],
                      phone=cleaned_data['phone'],
                      email=cleaned_data['email'],
                      city=cleaned_data['city'],
                      zip_code=cleaned_data['zip_code'],
                      zip_code_city=cleaned_data['zip_code_city'],
                      payment_method=cleaned_data['payment_method'],
                      order_status=1,
                      )
        order.save()
        cart = Cart(request)
        for item in cart:
            order_product = OrderProducts(order=order,
                                          pair=item['pair'],
                                          quantity=item['quantity'],
                                          price=item['price'])
            order_product.save()
        cart.clear()
        return HttpResponseRedirect(reverse_lazy('orders:order_list'))


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
