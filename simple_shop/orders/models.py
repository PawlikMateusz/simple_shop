from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Order(models.Model):
    ORDER_CODE = (
        ('1', 'Waiting for payment'),
        ('2', 'Paid'),
        ('3', 'Sent'),
        ('4', 'Delivered'),
    )
    PAYMENT_METHOD = (
        ('1', 'Traditional transfer'),
        ('2', 'Paypal'),
        ('3', 'Online transfer'),
        ('4', 'Cash on delivery'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=6)
    zip_code_city = models.CharField(max_length=30)
    payment_method = models.CharField(
        max_length=1, choices=PAYMENT_METHOD, default='1')
    order_status = models.CharField(
        max_length=1, choices=ORDER_CODE, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total_price = 0
        for ordered_product in self.products:
            total_price += ordered_product.quantity * ordered_product.price
        return total_price


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0, message='Quantity must bigger than 0')])
    price = models.DecimalField(decimal_places=2, max_digits=5, validators=[
        MinValueValidator(0, message='Price must bigger than 0')])
