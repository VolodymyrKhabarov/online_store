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

from orders.forms import ReturnPurchaseForm
from orders.models import PurchaseModel, ReturnPurchaseModel
from users.models import UserModel

# Define constants for error messages
REQUEST_ACCEPTED_MSG = "Your request has been accepted"
RETURN_PERIOD_ENDED_MSG = "Return period ended"


class PurchaseListView(LoginRequiredMixin, ListView, FormView):
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
        if purchase.purchased_at + timedelta(seconds=180) > timezone.now():
            messages.info(request=self.request, message=REQUEST_ACCEPTED_MSG)
            ReturnPurchaseModel.objects.create(product=purchase)
            return redirect("orders")
        else:
            messages.info(request=self.request, message=RETURN_PERIOD_ENDED_MSG)
            return redirect("orders")


class RefundListView(PermissionRequiredMixin, ListView):
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
