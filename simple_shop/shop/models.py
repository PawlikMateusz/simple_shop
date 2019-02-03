from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404

from PIL import Image
# Create your models here.


class Category(models.Model):
    SEX_CHOICES = ((True, 'Female'), (False, 'Male'))
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    sex = models.BooleanField(choices=SEX_CHOICES)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Discount(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(
        validators=[MinValueValidator(0, message='Percent value must bigger than 0'),
                    MaxValueValidator(100, message='100 perecent is maxiumum')])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=5,
                                validators=[MinValueValidator(0, message='Price must bigger than 0')])
    discount = models.ForeignKey(
        Discount, on_delete=models.PROTECT, related_name='products', blank=True, null=True)

    @property
    def discount_price(self):
        if not self.discount:
            return False
        result = float(self.price) * ((100-self.discount.value)/100)
        return '{:.2f}'.format(round(result, 2))

    @property
    def amount(self):
        pairs = Pair.objects.filter(product=self)
        result = 0
        for pair in pairs:
            result += pair.quantity
        return result

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


def upload_path_handler(instance, filename):
    return "products/{0}/{1}".format(instance.product.id, filename)


class ProductImages(models.Model):
    MAIN_IMAGE_CHOICE = ((True, 'Yes'), (False, 'No'))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_path_handler,
                              default='products/default.jpg')
    main_image = models.BooleanField(choices=MAIN_IMAGE_CHOICE, default=False)

    def image_tag(self):
        if 'default' in self.image.url:
            return 'Default image'
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))

    image_tag.short_description = 'Image'

    def __str__(self):
        return str(self.image.url)

    def save(self, *args, **kwargs):
        super(ProductImages, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.image.path)


class Pair(models.Model):
    number = models.DecimalField(max_digits=3, decimal_places=1, validators=[
        MinValueValidator(0, message='Number must bigger than 0')])
    quantity = models.IntegerField(
        validators=[MinValueValidator(0, message='Quantity must bigger than 0')])
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='available_pairs')

    @property
    def get_available_pair(self):
        if str(self.number)[-1] == '0':
            return str(self.number)[:-2]
        return str(self.number)

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ['number']
