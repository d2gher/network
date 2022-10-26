from urllib.request import HTTPRedirectHandler
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = []
    try: 
        posts = Post.objects.all()
    except: 
        return

    return render(request, "network/index.html", {
        "posts": posts 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def posts(request):
    if request.method == "POST":
        if not (request.user.is_authenticated):
            return 

        username = request.user.username
        body = request.POST["body"]
        try: 
            user = User.objects.get(username=username)
            post = Post(user=user, body=body)
            post.save()
        except: 
            return render(request, "network/index.html", {
                "message": "An error occurred"
            })

        return HttpResponseRedirect("/")    

def profile(request, username):
    try: 
        user = User.objects.get(username=username)
        posts = Post.objects.all().filter(user=user)
        
    except:
        return render(request, "network/profile.html", {
        "message": "User doesn't exist"
    })      

    return render(request, "network/profile.html", {
        "posts": posts,
        "username": username
    })