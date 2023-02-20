"""
This module for processing user requests and returning responses.
"""

from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView

from orders.models import PurchaseModel
from orders.forms import PurchaseForm
from products.forms import CreateProductForm, EditProductForm
from products.models import ProductModel
from users.models import UserModel


# Define constants for messages
INVALID_FORM_MSG = "Form is invalid. Please correct the errors."
NOT_AVAILABLE_MSG = "Not available in this quantity"
NOT_ENOUGH_MONEY_MSG = "Not enough money"
SUCCESS_CREATE_MSG = "Product created successfully"
SUCCESS_EDIT_MSG = "Product has been updated successfully"
SUCCESS_PURCHASE_MSG = "Your purchase was successful"


class ProductListView(FormView):
    """
    Class-based view for displaying a list of products and processing purchase forms.
    """

    form_class = PurchaseForm
    success_url = reverse_lazy("list")
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductModel.objects.all()
        return context

    def form_valid(self, form):
        try:
            product = get_object_or_404(ProductModel, pk=self.request.POST["pk"])
        except HttpResonseNotFound:
            messages.error(self.request, PRODUCT_NOT_FOUND_MSG)
            return redirect("list")

        if int(self.request.POST.get("amount")) > product.quantity:
            messages.error(self.request, NOT_AVAILABLE_MSG)
            return redirect("list")
        else:
            amount = int(self.request.POST.get("amount"))
            price = Decimal(str(product.price)) * amount
            if self.request.user.wallet < price:
                messages.error(self.request, NOT_ENOUGH_MONEY_MSG)
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
                messages.success(self.request, SUCCESS_PURCHASE_MSG)
                return super(ProductListView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, INVALID_FORM_MSG)
        return self.render_to_response(self.get_context_data(form=form))


class EditProductView(PermissionRequiredMixin, UpdateView):
    """
    A view for editing a product. This view is accessible for admin role only.
    """

    model = ProductModel
    permission_required = "is_superuser"
    form_class = EditProductForm
    template_name = "edit.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        messages.success(self.request, SUCCESS_EDIT_MSG)
        return super().form_valid(form)


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
        messages.success(self.request, SUCCESS_CREATE_MSG)
        return super(CreateProductView, self).form_valid(form)
