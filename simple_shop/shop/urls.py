from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="shop/home.html"), name="home"),
    path("text/", TemplateView.as_view(template_name="shop/test.html"), name="home"),

]
