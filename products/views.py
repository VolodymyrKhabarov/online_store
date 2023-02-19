"""
This module for processing user requests and returning responses.
"""

from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, FormView

from products.forms import CreateProductForm, EditProductForm
from products.models import ProductModel
from users.models import UserModel

# Define constants for error messages
NOT_AVAILABLE_MSG = "Not available in this quantity"
NOT_ENOUGH_MONEY_MSG = "Not enough money"


class ProductListView(ListView):
    model = ProductModel
    template_name = "product_list.html"
    context_object_name = "products"

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id", "")
        amount = int(request.POST.get("amount", ""))
        user_id = int(request.POST.get("user_id", ""))

        user = UserModel.objects.get(pk=user_id)
        product = ProductModel.objects.get(pk=product_id)

        product.quantity -= amount
        user.wallet = Decimal(user.wallet) - amount * Decimal(product.price)

        if product.quantity < 0:
            messages.add_message(request, messages.ERROR, NOT_AVAILABLE_MSG)
        elif user.wallet < 0:
            messages.add_message(request, messages.ERROR, NOT_ENOUGH_MONEY_MSG)
        else:
            purchase = PurchaseModel(user_id=user, product_id=product, amount=amount)
            user.save()
            product.save()
            purchase.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class EditProductView(PermissionRequiredMixin, UpdateView):
    model = ProductModel
    permission_required = "is_superuser"
    form_class = EditProductForm
    template_name = "edit.html"
    success_url = reverse_lazy("list")


class CreateProductView(PermissionRequiredMixin, FormView):
    model = ProductModel
    permission_required = "is_superuser"
    form_class = CreateProductForm
    template_name = "add.html"
    fields = ["name", "price", "amount", "description"]
    success_url = reverse_lazy("add")

    def form_valid(self, form):
        ProductModel.objects.create(
            name=self.request.POST["name"],
            description=self.request.POST["description"],
            price=self.request.POST["price"],
            quantity=self.request.POST["quantity"]
        )
        return super(CreateProductView, self).form_valid(form)
