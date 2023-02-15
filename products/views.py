"""
This module for processing user requests and returning responses.
"""

from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy

from products.models import ProductModel
from products.forms import EditProductForm


class ProductListView(ListView):
    model = ProductModel
    template_name = "product_list.html"
    context_object_name = "products"


class EditProductView(UpdateView):
    model = ProductModel
    form_class = EditProductForm
    template_name = "edit.html"
    success_url = reverse_lazy("list")