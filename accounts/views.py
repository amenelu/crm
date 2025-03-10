from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.filters import OrderFilter
from .models import *
from .forms import OrderForms, CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + username)
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "username or password incorrect")
    context = {}
    return render(request, "accounts/login.html", context)


def logoutuser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    Total_orders = orders.count()
    Orders_delivered = orders.filter(status="Delivered").count()
    Total_customers = customers.count()
    Pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "customers": customers,
        "Total_orders": Total_orders,
        "orders_delivered": Orders_delivered,
        "Total_customers": Total_customers,
        "pending": Pending,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def userPage(request):
    # customer = getattr(request.user, "customer", None)
    orders = request.user.customer.order_set.all()
    Total_orders = orders.count()
    Orders_delivered = orders.filter(status="Delivered").count()
    Pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "Total_orders": Total_orders,
        "orders_delivered": Orders_delivered,
        "pending": Pending,
    }
    return render(request, "accounts/userpage.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "accounts/accounts_settings.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {"products": products})


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        "customer": customer,
        "orders": orders,
        "order_count": order_count,
        "myFilter": myFilter,
    }
    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer,
        Order,
        fields=(
            "product",
            "status",
        ),
        extra=5,
    )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForms(initial={"customer": customer})
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {"formset": formset}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForms(instance=order)

    if request.method == "POST":
        form = OrderForms(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}

    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context = {"item": order}
    return render(request, "accounts/delete.html", context)


# Create your views here.
