from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

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

    return render(request, 'login.html', {"hide_menu": True})
