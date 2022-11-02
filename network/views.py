from ast import parse
from telnetlib import STATUS
from urllib.request import HTTPRedirectHandler
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect

from .models import Like, User, Post, Follow

paginator_limit = 10

def index(request):
    posts = []
    page_number = 1
    try: 
        user = User.objects.get(username=request.user.username)
        posts = Post.objects.all().order_by('-timestamp')
        posts = Paginator(posts, paginator_limit) 
        pages_len = posts.num_pages
        page_number = request.GET.get('page')
        page_objs = posts.get_page(page_number)
        for post in page_objs:
            try: 
                Like.objects.get(user=user, post=post)
                setattr(post, "liked", True)
            except:
                setattr(post, "liked", False)    

        return render(request, "network/index.html", { "posts": page_objs, "pages_len": range(pages_len) })

    except: 
        return render(request, "network/index.html", { "message": "No posts found" })

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

@csrf_exempt
@login_required
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

        return HttpResponseRedirect(reverse("index"))

    if request.method == "PUT":
        data = json.loads(request.body)
        try: 
            post = Post.objects.get(id=data.get("id"))
            if request.user.username != str(post.user):
                raise Exception("The loged in user isn't the owner of the post")
            post.body = data.get("body")
            post.save()  
            return JsonResponse({
                "error": "Post updated"
            }, status=200)  
        except: 
            return JsonResponse({
                "error": "PUT Request couldn't be processed."
            }, status=400) 

    if request.method == "GET":
        try:
            post_id = request.GET.get('post')
            post = Post.objects.get(id=post_id)
            return JsonResponse({"likes": post.likes}, status=200)
        except:
            return JsonResponse({"Error": "Couldn't find the post"}, status=404)    


def profile(request, username):
    try: 
        following = False
        user = User.objects.get(username=username)
        posts = Post.objects.all().filter(user=user).order_by('-timestamp')
        posts = Paginator(posts, paginator_limit) 
        pages_len = posts.num_pages
        page_number = request.GET.get('page')
        page_objs = posts.get_page(page_number)
    except:
        return render(request, "network/profile.html", {
        "message": "User doesn't exist"
    })      

    try:
        if request.user.is_authenticated: 
            cUser = User.objects.get(username=request.user.username)
            following = Follow.objects.get(follower=cUser, following=user)
            if following:
                following = True
    except: 
        following = False            
    return render(request, "network/profile.html", { "posts": page_objs, "pages_len": range(pages_len), "username": username, "following": following })
    
def follow(request, username):
    if request.method == "POST":
        if not (request.user.is_authenticated):
            return 

        try:
            follower = User.objects.get(username=request.user.username)
            following = User.objects.get(username=username)
        except: 
            return render(request, "network/profile.html", {"message": "User doesn't exist"})

        
        if request.POST["action"] == "follow":
            try:
                Follow.objects.get(follower=follower, following=following)     
            except:
                follow = Follow(follower=follower, following=following)
                follow.save()

        if request.POST["action"] == "unfollow":
            try:
                follow = Follow.objects.get(follower=follower, following=following)
                follow.delete()  
            except:
                return render(request, "network/profile.html", { "message": "User doesn't exist"})  
                
        return HttpResponseRedirect(f"/{username}")   

def following(request, username=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login")) 


    if request.method == "GET":
        
        posts = []
        try: 
            user = User.objects.get(username=request.user.username)
            following = list(Follow.objects.filter(follower=user).values_list('following', flat=True))
            posts = Post.objects.all().order_by('-timestamp')
            posts_list = posts.values()
            if not posts: 
                return render(request, "network/index.html", { "message": "No posts found" })

            following_posts = []
            for post in posts_list: 
                if post["user_id"] in following:
                    owner = User.objects.get(id=post["user_id"])
                    post.update({"user": owner})
                    following_posts.append(post)
                    
            following_posts = Paginator(following_posts, paginator_limit) 
            pages_len = following_posts.num_pages
            page_number = request.GET.get('page')
            page_objs = following_posts.get_page(page_number)

            return render(request, "network/index.html", { "posts": page_objs, "pages_len": range(pages_len) })   
           
        except: 
            return render(request, "network/index.html", { "message": "No posts found1" })   

@csrf_exempt
@login_required
def likes(request):
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            print(data)
            post_id = data.get("post_id")
            post = Post.objects.get(id=post_id)
            user = User.objects.get(username=request.user.username)
        except: 
            return JsonResponse({ "error": "Couldn't find user or post" }, status=400)

        try:
            like = Like.objects.get(post=post, user=user)
            post.likes -= 1
            post.save()
            like.delete()
            return JsonResponse({ "success": "Post unliked" }, status=200)  
        except:
            like = Like(post=post, user=user)
            like.save()
            post.likes += 1
            post.save()
            return JsonResponse({ "success": "Post liked" }, status=200)  
    return JsonResponse({ "success": "get out" }, status=200)  
            

