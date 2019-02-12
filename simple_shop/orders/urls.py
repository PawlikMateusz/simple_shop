from django.urls import path

from .views import TestTemplateView

app_name = 'orders'

urlpatterns = [
    path('', TestTemplateView.as_view(), name='test_view'),
]
