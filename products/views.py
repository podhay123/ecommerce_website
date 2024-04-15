from multiprocessing import context
from unicodedata import name
from django.shortcuts import render
from . import models
from shopping_cart.models import Order
from django.contrib.auth.decorators import login_required
from products.forms import CommentForm
from django.contrib.auth.models import User
from users.models import Profile

# def all_products(request):
#     products = models.Product.objects.all().order_by("name")
#     return render(request, "products/index.html", {"products": products})


@login_required(login_url="/users/login/")
def all_products(request):
    products = models.Product.objects.all().order_by("name")
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)

    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
    form = CommentForm
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
            item.user = request.user.profile
            item.save()

            products[0].comments.add(item)

        else:
            print("Invalid Form")
    context = {
        "products": products,
        "current_order_products": current_order_products,
        "form": form,
    }
    return render(request, "products/index.html", context)
