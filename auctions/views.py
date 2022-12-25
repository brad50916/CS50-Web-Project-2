from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import User, List, Bid, Comment, Watchlist
from django.contrib.auth.decorators import login_required
from django import forms

class createform(forms.Form):
    options = (
        ('el', 'Electronics'),
        ('to', 'Toys'),
        ('fa', 'Fashion'),
        ('fu', 'Furnitures'),
        ('be', 'Beauty, health, and household care'),
        ('other', 'Others'),
    )
    product = forms.CharField(label="Product Name")
    price = forms.IntegerField(label="Price")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    url = forms.CharField(label="url", required=False)
    category = forms.ChoiceField(choices=options)
    def __init__(self, *args, **kwargs):
        super(createform, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['style'] = 'width:200px; height:25px; display:block'
        self.fields['price'].widget.attrs['style'] = 'width:200px; height:25px; display:block'
        self.fields['description'].widget.attrs['style'] = 'width:700px; height:200px; display:block'
        self.fields['url'].widget.attrs['style'] = 'width:200px; height:25px; display:block'
        self.fields['category'].widget.attrs['style'] = 'width:200px; height:25px; display:block'


def index(request):
    if request.user.is_authenticated:
        id = request.user.id
        return render(request, "auctions/index.html", {
        "list": List.objects.all(),
        "id": id
    })
    return render(request, "auctions/index.html", {
        "list": List.objects.all()
    })

@login_required(login_url='login')
def create(request):
    id=request.user.id 

    form = createform(request.POST)
    if form.is_valid():
        product=form.cleaned_data["product"]
        price=form.cleaned_data["price"]
        des=form.cleaned_data["description"]
        url=form.cleaned_data["url"]
        category=form.cleaned_data["category"]

        name = request.user
        f = List(product=product, price=price, des=des, 
        url=url, date=datetime.now(), user=name, category=category)
        f.save()
        b = Bid(product=f)
        b.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html",{
        "id": id,
        "form1": createform()
    })

def listing(request, list_id):

    list = List.objects.get(pk=list_id)
    bid = Bid.objects.get(product=list)
    
    com=0
    try:
        com = Comment.objects.filter(product=list)
        cexist=1
    except Comment.DoesNotExist:
        cexist=0

    if request.user.is_authenticated:
        user = request.user
        id=request.user.id
        try:
            Watchlist.objects.get(user=user, watchlist=list)
            exist=1
        except Watchlist.DoesNotExist:
            exist=0

        if request.method == "POST":
            if 'bid' in request.POST:
                if int(request.POST["bid"]) > list.price:
                    bid.user=user
                    bid.save()
                    list.price=request.POST["bid"]
                    list.save()
                    return render(request, "auctions/listing.html", {
                            "list": list,
                            "bid": bid,
                            "message1": "Successful bid.",
                            "id": id,
                            "exist": exist,
                            "comment": com,
                            "cexist": cexist
                    }) 
                else:
                    return render(request, "auctions/listing.html", {
                        "list": list,
                        "bid": bid,
                        "message2": "Invalid bid price.",
                        "id": id,
                        "exist": exist,
                        "comment": com,
                        "cexist": cexist
                    })
            elif 'close' in request.POST:
                list.close=1
                list.save()
                return render(request, "auctions/listing.html", {
                    "list": list,
                    "bid": bid,
                    "id": id,
                    "exist": exist,
                    "comment": com
                })
            elif 'comment' in request.POST:
                c = Comment(product=list, comment=request.POST["comment"], user=user)
                c.save()
                com = Comment.objects.filter(product=list)
                cexist = 1
                return render(request, "auctions/listing.html", {
                    "list": list,
                    "bid": bid,
                    "id": id,
                    "exist": exist,
                    "comment": com,
                    "cexist": cexist
                })
                
        return render(request, "auctions/listing.html", {
            "list": list,
            "bid": bid,
            "id": id,
            "exist": exist,
            "comment": com,
            "cexist": cexist
        })

    else:
        if request.method == "POST":
            if 'bid' in request.POST:
                return render(request, "auctions/listing.html", {
                    "list": list,
                    "bid": bid,
                    "message2": "You need login to place bid.",
                    "comment": com,
                    "cexist": cexist
                })
            elif 'comment' in request.POST:
                return render(request, "auctions/listing.html", {
                    "list": list,
                    "bid": bid,
                    "message3": "You need login to submit your comment.",
                    "comment": com,
                    "cexist": cexist
                })
        else:
            return render(request, "auctions/listing.html", {
                "list": list,
                "bid": bid,
                "comment": com,
                "cexist": cexist
            })

@login_required(login_url='login')
def watchlist(request, user_id):
    user=request.user
    if request.method == "POST":
        product_id=request.POST["id"] 
        list = List.objects.get(pk=product_id)
        w = Watchlist(user=user, watchlist=list)
        w.save()
    wl=Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "id": user_id,
        "watchlist": wl
    })

@login_required(login_url='login')
def rwatchlist(request, user_id):
    user=request.user
    if request.method == "POST":
        product_id=request.POST["id"] 
        list = List.objects.get(pk=product_id)
        Watchlist.objects.get(user=user, watchlist=list).delete()
        wl=Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "id": user_id,
        "watchlist": wl
    })

def category(request):
    id=request.user.id 
    if request.method == "POST":
        cate=List.objects.filter(category=request.POST["cate"])
        print(cate)
        return render(request, "auctions/category.html", {
            "id": id,
            "list": cate
        })
    return render(request, "auctions/category.html", {
            "id": id
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {
        })


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
                "message": "Passwords must match.",
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
        })
