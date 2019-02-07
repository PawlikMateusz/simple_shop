from django.contrib import admin

from .models import Category, Product, ProductImage
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'description', 'price']
    list_display = ['name', 'description', 'price']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'sex']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
