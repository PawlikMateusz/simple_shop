from django import forms
from django.utils.safestring import mark_safe
from django.contrib import messages

from . import utils
from .models import Product, Category, ProductImage, Pair


class ProductForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = ['category', 'name', 'description',  'price']
        labels = {
            "category": mark_safe("Select category or <a href='http://localhost:8000/add-category/'> create new one</a>"),
        }
        widgets = {'description': forms.Textarea(
            attrs={'cols': 80, 'rows': 15}), }


class BaseProductImageFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = ProductImage.objects.none()


class BasePairFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Pair.objects.none()
        self.forms[0].empty_permitted = False

    def clean(self):
        if any(self.errors):
            return
        utils.validate_pair_number(self.forms)


ProductImageFormSet = forms.modelformset_factory(
    ProductImage, formset=BaseProductImageFormSet, fields=('image', 'main_image'), extra=5)
PairFormSet = forms.modelformset_factory(
    Pair, formset=BasePairFormSet, fields=('number', 'quantity'), extra=5)
