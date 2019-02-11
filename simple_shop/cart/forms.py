from django import forms
from django.apps import apps

Pair = apps.get_model('shop', 'Pair')


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddPairForm(forms.Form):
    pair = forms.ModelChoiceField(queryset=Pair.objects.all())
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, product=None, *args, **kwargs):
        super(CartAddPairForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['pair'].queryset = Pair.objects.filter(
                product=product)

    def clean(self):
        cleaned_data = super().clean()
        pair = cleaned_data.get("pair")
        quantity = cleaned_data.get("quantity")
        if quantity > pair.quantity:
            raise forms.ValidationError(message='To many pairs')
