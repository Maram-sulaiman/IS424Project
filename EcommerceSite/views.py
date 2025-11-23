from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import user
from .forms import RegisterForm


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
