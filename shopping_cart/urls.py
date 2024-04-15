from django.urls import path
from . import views

app_name = "shopping_cart"

urlpatterns = [
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("order-summary/", views.order_details, name="order_summary"),
    path("success", views.success, name="purchase_success"),
    path("item/delete/<int:product_id>/", views.delete_from_cart, name="delete_item"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<int:order_id>/", views.process_payment, name="process_payment"),
    path(
        "update-transaction/<int:order_id>/",
        views.update_transaction_records,
        name="update_records",
    ),
]
