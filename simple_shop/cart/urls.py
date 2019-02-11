from django.urls import path

from .views import cart_add, cart_detail, cart_remove

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/', cart_add, name='cart_add'),
    path('remove/<pair>/', cart_remove, name='cart_remove'),
]
