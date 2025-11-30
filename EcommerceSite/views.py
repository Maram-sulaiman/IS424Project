from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Product, OrderedProduct,Order


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

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return HttpResponseRedirect(reverse("login"))


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
            return HttpResponseRedirect(reverse('login')) 
    else:
        form = RegisterForm()

    return render(request, 'Register.html', {
                "form": form,
                "hide_menu": True
            })

def products_view(request):
    products= Product.objects.all()
    return render(request, 'products.html', {
        "products":products
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        amount = int(request.POST.get("amount", 1))
        basket = request.session.get("basket", {})

        if str(id) in basket:
            basket[str(id)]["quantity"] += amount
        else:
            basket[str(id)] = {
                "name": product.name,
                "price": product.price,
                "quantity": amount
            }

        request.session["basket"] = basket
        return HttpResponseRedirect(reverse("product_details", args=[id]))

    return render(request, "product_detail.html", {"product": product})

def add_to_basket(request, product_id):
    product = Product.objects.get(id=product_id)

    basket = request.session.get("basket", {})

    if str(product_id) in basket:
        basket[str(product_id)]["quantity"] += 1
    else:
        basket[str(product_id)] = {
            "name": product.name,
            "price": product.price,
            "quantity": 1
        }
    request.session["basket"] = basket

    return HttpResponseRedirect(reverse("basket"))

def basket_page(request):
    basket = request.session.get("basket", {})

    total = sum(item["price"] * item["quantity"] for item in basket.values())

    return render(request, "basket.html", {
        "basket": basket,
        "total": total
    })

def update_quantity(request, product_id):
    basket = request.session.get("basket", {})

    if request.method == "POST":
        new_quantity = int(request.POST["quantity"])

        if new_quantity <= 0:
            basket.pop(str(product_id), None)
        else:
            basket[str(product_id)]["quantity"] = new_quantity

    request.session["basket"] = basket
    return HttpResponseRedirect(reverse("basket"))

def remove_item(request, product_id):
    basket = request.session.get("basket", {})

    if str(product_id) in basket:
        basket.pop(str(product_id))

    request.session["basket"] = basket
    return HttpResponseRedirect(reverse("basket"))

def clear_basket(request):
    request.session["basket"] = {}
    return HttpResponseRedirect(reverse("basket"))

def order_page(request):
    
    basket = request.session.get("basket", {})
    total = 0
    for item in basket.values():
        total += item["price"] * item["quantity"]

    
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )
        for product_id, item in basket.items():
            OrderedProduct.objects.create(
                user=request.user,
                product_id=product_id,
                amount=item["quantity"]
            )

        request.session["basket"] = {}
        return render(request, "order_success.html", {
            "order": order
        })

    return render(request, "order.html", {
        "basket": basket,
        "total": total
    })
