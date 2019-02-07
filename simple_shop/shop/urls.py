from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    CategoryCreateView,
    ProductListView,
    ProductAddWizard,
    ManageTemplateView
)
from .forms import ProductForm, ProductImageFormSet, PairFormSet


app_name = 'shop'

urlpatterns = [
    path("", ProductListView.as_view(), name="home_view"),
    path('manage', ManageTemplateView.as_view(), name='manage_view'),
    path('products/', ProductAddWizard.as_view(
        [ProductForm, ProductImageFormSet, PairFormSet]), name='product_add_view'),
    path('add-category', CategoryCreateView.as_view(), name='category_add_view'),
]
