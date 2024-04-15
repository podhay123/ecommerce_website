from audioop import reverse
from datetime import datetime
from multiprocessing import context
from users.models import Profile
from products.models import Product
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem


@login_required(login_url="/users/login/")
def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required(login_url="/users/login/")
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get("product_id", "")).first()
    # checks if the user already owns this product
    if product in request.user.profile.products.all():
        messages.info(request, "You already own this product")
        return redirect("products:all_products")
    # create OrederItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(
        owner=user_profile, is_ordered=False
    )
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        # user_order.ref_code = generate_order_id()
        user_order.save()
    # show comfirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect("products:all_products")


@login_required(login_url="/users/login/")
def delete_from_cart(request, product_id):
    item_to_delete = OrderItem.objects.filter(pk=product_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "item has been deleted")
    return redirect("products:all_products")


@login_required(login_url="/users/login/")
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {"order": existing_order}
    return render(request, "shopping_cart/order_summary.html", context)


@login_required(login_url="/users/login/")
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {"order": existing_order}
    return render(request, "shopping_cart/checkout.html", context)


@login_required(login_url="/users/login/")
def process_payment(request, order_id):
    return redirect(
        reverse("products:index"),
        kwargs={
            "order_id": order_id,
        },
    )


@login_required(login_url="/users/login/")
def update_transaction_records(request, order_id):
    # get the oreder being processed
    order_to_pucharse = Order.objects.filter(pk=order_id).filter()

    # update placed order
    order_to_pucharse.is_ordered = True
    order_to_pucharse.date_ordered = datetime.datetime.now()
    order_to_pucharse.save()

    # get all items in the order
    order_items = order_to_pucharse.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.products.add(*order_products)
    user_profile.save()

    # TODO UPDATE PAYMENT RECORDS

    # send email to customer
    messages.info(request, "Thank you! Your items have been added to your profile")
    return redirect(reverse("accounts:profile"))


def success(request, **kwargs):
    return render(request, "shopping_cart/purchase_success.html", {})
