from .models import Category


def product_categories(request):
    female_categories = Category.objects.filter(sex=True)
    male_categories = Category.objects.filter(sex=False)
    return {"female_categories": female_categories, "male_categories": male_categories}
