from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView

import os
import shutil

from cart.forms import CartAddPairForm
from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageFormSet, PairFormSet

# Create your views here.


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'shop/home.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddPairForm(self.object)
        return context


class ManageTemplateView(TemplateView):
    template_name = 'shop/staff_sites/manage.html'


class ProductAddWizard(SessionWizardView):
    template_name = 'shop/staff_sites/product_add_wizard.html'
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def done(self, form_list, **kwargs):
        product_form = list(form_list)[0]
        product = product_form.save()
        product.save()
        images_formset = list(form_list)[1]
        images = images_formset.save(commit=False)
        if images:
            for image in images:
                image.product = product
                image.save()
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'photos'))
        else:
            image = ProductImage(product=product)
            image.save()
        pairs_formset = list(form_list)[2]
        pairs = pairs_formset.save(commit=False)
        for pair in pairs:
            pair.product = product
            pair.save()
        messages.success(self.request, message='Product added successfully')
        return redirect('shop:home_view')


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name', 'sex']
    success_url = reverse_lazy('shop:product_add_view')
    success_message = "Category was created successfully"


class CategoryProductsListView(ListView):
    model = Product
    template_name = 'shop/products_in_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['product_list'] = Product.objects.filter(
            category=category).order_by('-id')
        context['category'] = category
        return context
