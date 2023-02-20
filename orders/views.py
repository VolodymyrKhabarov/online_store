"""
This module for processing user requests and returning responses.
"""

from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, FormView

from orders.forms import ReturnPurchaseForm
from orders.models import PurchaseModel, ReturnPurchaseModel
from users.models import UserModel


# Define constants for error messages
REQUEST_ACCEPTED_MSG = "Your request has been accepted"
RETURN_PERIOD_ENDED_MSG = "The return period for this purchase has ended"
REJECT_RE_RETURN_MSG = "You have already requested a return for this purchase"


class PurchaseListView(LoginRequiredMixin, ListView, FormView):
    """
    A view that displays a list of purchases made by users and provides an option to return products.
    """

    model = PurchaseModel
    template_name = "orders.html"
    context_object_name = "orders"
    ordering = "-purchased_at"
    form_class = ReturnPurchaseForm
    success_url = reverse_lazy("orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for order in context["orders"]:
            order.total_price = order.amount * order.product_id.price
        return context

    def form_valid(self, form):
        purchase = PurchaseModel.objects.get(pk=self.request.POST["pk"])
        try:
            ReturnPurchaseModel.objects.get(product=purchase)
            messages.info(request=self.request, message=REJECT_RE_RETURN_MSG)
        except ReturnPurchaseModel.DoesNotExist:
            if purchase.purchased_at + timedelta(seconds=180) > timezone.now():
                messages.info(request=self.request, message=REQUEST_ACCEPTED_MSG)
                ReturnPurchaseModel.objects.create(product=purchase)
            else:
                messages.info(request=self.request, message=RETURN_PERIOD_ENDED_MSG)
        return redirect("orders")


class RefundListView(PermissionRequiredMixin, ListView):
    """
    A view for displaying a list of refunds of purchased products. Only users with the "is_superuser" permission are
    allowed to access this view.

    Methods:
        post(self, request, *args, **kwargs): Handles the POST request to confirm a refund. Retrieves the refund to be
        processed and updates the user's wallet and the product's quantity and saves the changes to the database.
        If the request is not to confirm a refund, it deletes the refund from the database.
    """

    model = ReturnPurchaseModel
    permission_required = "is_superuser"
    context_object_name = "refunds"
    ordering = "requested_at"
    template_name = "refunds.html"

    def post(self, request, *args, **kwargs):
        refund_id = request.POST.get("refund_id", "")
        refund = ReturnPurchaseModel.objects.get(pk=refund_id)

        if "confirm" in request.POST:

            refund.product.user_id.wallet = Decimal(refund.product.user_id.wallet) + refund.product.amount * \
                                            refund.product.product_id.price
            refund.product.user_id.save()
            refund.product.product_id.quantity += refund.product.amount
            refund.product.product_id.save()
        refund.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
