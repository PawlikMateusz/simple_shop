from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import OrderFormPreview, OrderListView
from .forms import OrderForm
app_name = 'orders'

urlpatterns = [
    path('create/', login_required(OrderFormPreview(OrderForm)), name='order_create'),
    path('list/', OrderListView.as_view(), name='order_list')
]
