from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class List(models.Model):
    product = models.CharField(max_length=64, default="")
    price = models.IntegerField()
    des = models.CharField(max_length=100, default="")
    url = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item", null=True)
    close = models.IntegerField(default=0) 
    category = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return f"{self.product} {self.price} {self.des} {self.url}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchuser", null=True)
    watchlist = models.ForeignKey(List, on_delete=models.CASCADE, related_name="watchproduct", null=True)

class Bid(models.Model):
    product = models.ForeignKey(List, on_delete=models.CASCADE, related_name="bid_product", null=True)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user", null=True, blank=True)
    def __str__(self):
        return f"{self.product}: {self.price}"

class Comment(models.Model):
    product = models.ForeignKey(List, on_delete=models.CASCADE, related_name="comment_product", null=True)
    comment = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user", null=True, blank=True)
    def __str__(self):
        return f"{self.product}: {self.comment}"