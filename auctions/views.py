from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Category


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : activeListings,
        "categories": categories
    })

def listing(request, id):
    procuctData = Listing.objects.get(pk=id)
    isWatchListed = request.user in procuctData.watchlist.all() if request.user else False
    return  render(request,"auctions/listing.html",{
        "products":procuctData,
        "watchStatus":isWatchListed 
    })

def addtoWatchlist(request, id):
    productData = Listing.objects.get(pk=id)
    currentuser = request.user
    productData.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def removeFromWatchlist(request, id):
    productData = Listing.objects.get(pk=id)
    currentuser = request.user
    productData.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
def watchList(request):
    currentUser = request.user
    userProducts = currentUser.watchlist.all()
    return render(request,"auctions/watchlist.html",{   
        "listings":userProducts
    })

def displaycategory(request):
    if request.method  == 'POST':
        categoryFromForm = request.POST['category']
        category =  Category.objects.get(name=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings" : activeListings,
            "categories": categories
        })


def createListing(request):
    if request.method ==  'GET':
        categories = Category.objects.all()
        return render(request, 'auctions/create_listing.html',{
            'categories' : categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']

        if price == '':
            return HttpResponse("Error: Price cannot be empty.")

        category = request.POST['category']
        categoryname= Category.objects.get(name=category)
        imgurl =  request.POST['image']
        
        user  = request.user

        listing = Listing(title=title,
                        description=description,
                        price = float(price),
                        imgUrl=imgurl,
                        category=categoryname,
                        owner = user)
        listing.save()
        return HttpResponseRedirect(reverse(index))
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
