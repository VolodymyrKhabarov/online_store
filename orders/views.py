"""
This module for processing user requests and returning responses.
"""

from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, FormView

from orders.forms import ReturnPurchaseForm
from orders.models import PurchaseModel, ReturnPurchaseModel


# Define constants for messages
PURCHASE_DOES_NOT_EXIST_MSG = "The purchase you are trying to return does not exist"
REQUEST_ACCEPTED_MSG = "Your request has been accepted"
RETURN_PERIOD_ENDED_MSG = "The return period for this purchase has ended"
REJECT_RE_RETURN_MSG = "You have already requested a return for this purchase"
SUCCESS_RETURN_MSG = "Request for product return has been successfully processed"
SUCCESS_REJECT_MSG = "Request for product return has been successfully rejected"


class PurchaseListView(LoginRequiredMixin, ListView, FormView):
    """
    A view that displays a list of purchases made by users and provides an option to return products
    """

    model = PurchaseModel
    template_name = "orders.html"
    context_object_name = "orders"
    ordering = "-purchased_at"
    form_class = ReturnPurchaseForm
    success_url = reverse_lazy("orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context.get("orders")
        if orders is not None:
            for order in orders:
                order.total_price = order.amount * order.product_id.price
        context["orders"] = orders
        return context

    def form_valid(self, form):
        try:
            purchase = PurchaseModel.objects.get(pk=self.request.POST["pk"])
        except PurchaseModel.DoesNotExist:
            messages.error(self.request, PURCHASE_DOES_NOT_EXIST_MSG)
            return redirect("orders")

        try:
            existing_return = ReturnPurchaseModel.objects.get(product=purchase)
            messages.info(self.request, REJECT_RE_RETURN_MSG)
        except ReturnPurchaseModel.DoesNotExist:
            try:
                if purchase.purchased_at + timedelta(seconds=180) > timezone.now():
                    ReturnPurchaseModel.objects.create(product=purchase)
                    messages.info(self.request, REQUEST_ACCEPTED_MSG)
                else:
                    messages.info(self.request, RETURN_PERIOD_ENDED_MSG)
            except Exception as err:
                messages.error(self.request, str(err))
                return redirect("orders")
        return redirect("orders")


class RefundListView(PermissionRequiredMixin, ListView):
    """
    A view for displaying a list of refunds of purchased products. Only users with
    the "is_superuser" permission are allowed to access this view.

    Methods:
        post(self, request, *args, **kwargs): Handles the POST request to confirm a refund.
        Retrieves the refund to be processed and updates the user's wallet and the product's
        quantity and saves the changes to the database.
        If the request is not to confirm a refund, it deletes the refund from the database.
    """

    model = ReturnPurchaseModel
    permission_required = "is_superuser"
    context_object_name = "refunds"
    ordering = "requested_at"
    template_name = "refunds.html"

    def post(self, request, *args, **kwargs):
        """
        Handles a POST request for refund confirmation or rejection.
        """

        refund_id = request.POST.get("refund_id", "")
        try:
            refund = ReturnPurchaseModel.objects.get(pk=refund_id)
        except ReturnPurchaseModel.DoesNotExist:
            return HttpResponseNotFound()

        if "confirm" in request.POST:
            refund.product.user_id.wallet = Decimal(refund.product.user_id.wallet) + \
                                            refund.product.amount * refund.product.product_id.price
            refund.product.user_id.save()
            refund.product.product_id.quantity += refund.product.amount
            refund.product.product_id.save()
            messages.success(request, SUCCESS_RETURN_MSG)
        else:
            messages.success(request, SUCCESS_REJECT_MSG)
        refund.delete()
        return redirect("refunds")
