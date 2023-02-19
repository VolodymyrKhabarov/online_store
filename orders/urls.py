"""
Orders URL Configuration
"""

from django.urls import path

from orders.views import PurchaseListView, RefundListView


urlpatterns = [
    path("orders", PurchaseListView.as_view(), name="orders"),
    path("refunds", RefundListView.as_view(), name="refunds")
]
