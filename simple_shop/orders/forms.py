from django import forms

from django.apps import apps

Order = apps.get_model('orders', 'Order')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'email', 'city',
                  'zip_code', 'zip_code_city', 'payment_method')

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) != 6:
            raise forms.ValidationError('Zip code should looks like "07-205"')
        if zip_code[2] != '-':
            raise forms.ValidationError('Zip code should looks like "07-205"')
        return zip_code
