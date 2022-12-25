from django.contrib import admin
from .models import User, List, Bid, Comment, Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(List)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)