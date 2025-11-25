from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Product, OrderedProduct


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('products')) 
        else:
            return render(request, 'login.html', {
                "error": "Invalid username or password",
                "hide_menu": True
            })

    return render(request, 'login.html', {
        "hide_menu": True
        })

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
    
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            User.objects.create_user(
                username=username,  password=password, email=email
            )
            return redirect(reverse('login')) 
    else:
        form = RegisterForm()

    return render(request, 'Register.html', {
                "form": form,
                "hide_menu": True
            })

def products_view(request):
    products= Product.objects.all()
    return render (request, 'products.html', {
        "products":products
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        amount = int(request.POST.get("amount", 1))

        basket_items = OrderedProduct.objects.filter(user=request.user, product=product)
        if len(basket_items) == 0:
            item = OrderedProduct(user=request.user, product=product, amount=amount)
            item.save()
        else:
            item = basket_items[0]
            item.amount = item.amount + amount
            item.save()

        return HttpResponseRedirect(reverse("basket"))

    return render(request, "product_detail.html", {"product": product})

