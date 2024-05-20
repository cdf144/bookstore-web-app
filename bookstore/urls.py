"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from products import views
from products.views import CheckoutView, CartView

app_name = "core"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", views.home, name="home"),
    path("categories/<int:category_id>/", views.category_books, name="category_books"),
    path("users/", views.users, name="users"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:id>/", views.book_detail, name="book_detail"),
    path("search/", views.search, name="search"),
    path("checkout/", CheckoutView.as_view(), name="check_out"),
    path("cart/", CartView.as_view(), name="cart"),
    path("add_to_cart<str:book_title>/", views.add_to_cart, name="add_to_cart"),
    path('profile/', views.profile, name='profile'),
    path("remove_from_cart/<str:book_title>/", views.remove_from_cart, name="remove_from_cart"),
    path("login/", views.login, name='login'),
    path('add_to_wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('profile/settings/', views.settings, name='settings'),
]
