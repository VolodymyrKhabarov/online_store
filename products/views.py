"""
This module for processing user requests and returning responses.
"""

from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView

from orders.models import PurchaseModel
from orders.forms import PurchaseForm
from products.forms import CreateProductForm, EditProductForm
from products.models import ProductModel
from users.models import UserModel


# Define constants for error messages
NOT_AVAILABLE_MSG = "Not available in this quantity"
NOT_ENOUGH_MONEY_MSG = "Not enough money"


class ProductListView(ListView, FormView):
    """
    Class-based view for displaying a list of products and processing purchase forms.
    """
    
    model = ProductModel
    form_class = PurchaseForm
    success_url = reverse_lazy("list")
    template_name = "product_list.html"
    context_object_name = "products"

    def form_valid(self, form):
        product = ProductModel.objects.get(pk=self.request.POST["pk"])
        if int(self.request.POST.get("amount")) > product.quantity:
            messages.add_message(self.request, messages.ERROR, NOT_AVAILABLE_MSG)
            return redirect("list")
        else:
            amount = int(self.request.POST.get("amount"))
            price = Decimal(str(product.price)) * amount
            if self.request.user.wallet < price:
                messages.error(request=self.request, message=NOT_ENOUGH_MONEY_MSG)
                return redirect("list")
            else:
                self.request.user.wallet = Decimal(str(self.request.user.wallet)) - price
                self.request.user.save()
                product.quantity -= amount
                product.save()
                PurchaseModel.objects.create(
                    user_id=self.request.user,
                    product_id=product,
                    amount=amount
                )
                return super(ProductListView, self).form_valid(form)


class EditProductView(PermissionRequiredMixin, UpdateView):
    """
    A view for editing a product. This view is accessible for admin role only.
    """

    model = ProductModel
    permission_required = "is_superuser"
    form_class = EditProductForm
    template_name = "edit.html"
    success_url = reverse_lazy("list")


class CreateProductView(PermissionRequiredMixin, FormView):
    """
    A view for creating new ProductModel objects by submitting a form. This view is accessible for admin role only.
    """

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
