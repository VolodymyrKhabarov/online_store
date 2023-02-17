"""
This module for processing user requests and returning responses.
"""

from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, FormView

from products.forms import EditProductForm, ReturnPurchaseForm
from products.models import ProductModel, PurchaseModel
from users.models import UserModel


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
            messages.add_message(request, messages.ERROR, "Not available in this quantity")
        elif user.wallet < 0:
            messages.add_message(request, messages.ERROR, "Not enough money")
        else:
            purchase = PurchaseModel(user_id=user, product_id=product, amount=amount)
            user.save()
            product.save()
            purchase.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class EditProductView(UpdateView):
    model = ProductModel
    form_class = EditProductForm
    template_name = "edit.html"
    success_url = reverse_lazy("list")


class PurchaseListView(ListView, FormView):
    model = PurchaseModel
    template_name = "orders.html"
    context_object_name = "orders"
    ordering = "-purchased_at"
    form_class = ReturnPurchaseForm
    success_url = reverse_lazy("orders")

    def form_valid(self, form):
        purchase = PurchaseModel.objects.get(pk=self.request.POST["pk"])
        if purchase.purchased_at + timedelta(seconds=180) > timezone.now():
            messages.info(request=self.request, message="Your request has been accepted")
            ReturnPurchase.objects.create(
                product=purchase)
            return redirect("orders")
        else:
            messages.info(request=self.request, message="Return period ended")
            return redirect("orders")
