from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<int:user_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:user_id>/rwatchlist", views.rwatchlist, name="rwatchlist"),
    path("category", views.category, name="category"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
