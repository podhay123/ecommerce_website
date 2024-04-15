from email import message
from multiprocessing import context
from django.shortcuts import render, redirect

# from shopping_cart.models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Profile
from shopping_cart.models import Order


# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Zarejstrowano poprawnie!")
            return redirect("products:all_products")
    else:
        form = UserCreationForm()
    return render(
        request,
        "users/authenticate/register_user.html",
        {
            "form": form,
        },
    )


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        passowrd = request.POST["password"]
        print(username, passowrd)
        user = authenticate(request, username=username, password=passowrd)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("products:all_products")
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect("users:login")
    else:
        return render(request, "users/authenticate/login_user.html", {})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out properly")
    return redirect("products:all_products")


def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {"my_orders": my_orders}
    return render(request, "profile.html", context)
