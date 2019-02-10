from decimal import Decimal
from django import forms


# FORMS VALIDATORS
def validate_pair_number(formset):
    def validate_number_format(number):
        if number % Decimal(0.5):
            raise forms.ValidationError(
                "Numbers must be divisible by 0.5")

    def check_for_duplicated_number(formset):
        added_numbers = []
        for form in formset:
            if form.cleaned_data:
                number = form.cleaned_data['number']
                validate_number_format(number)
                if number in added_numbers:
                    raise forms.ValidationError(
                        "There are two or more the same pair numbers. Please correct this :)")
                added_numbers.append(number)

    check_for_duplicated_number(formset)
