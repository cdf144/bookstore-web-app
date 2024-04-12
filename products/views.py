from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from models import Book, CartItems, Cart, UserAddress
from datetime import datetime, timezone
# Create your views here.
@login_required
def add_to_cart(request, book, user):
    carts = Cart.objects.get_object_or_404(user=user)
    if carts.exists():
        cart = carts[0]
        cartItems = CartItems.objects.filter(cart=cart, book=book).first()
        if cartItems.exists():
            cartItems.quantity += 1
            cartItems.save()
            messages.info(request, 'Book quantity updated')
        else:
            cartItems.objects.create(cart=cart,book=book, quantity=1)
            messages.info(request, 'Succesfully added book')
    else:
        currTime = timezone.now()
        cart = Cart.objects.create(created_by=user, create_at=currTime)
        cartItems = CartItems.objects.create(cart=cart, book=book, quantity=1)
        messages.info(request, 'Succesfully added book')

@login_required
def remove_from_cart(request, book, user):
    carts = Cart.objects.get_object_or_404(user=user)
    if carts.exists():
        cart = carts[0]
        try:
            cartItem = CartItems.objects.filter(cart=cart, book=book).first()
            if cartItem.quantity == 0:
                cartItem.delete()
                messages.info(request, 'Removed book from cart')
            else:
                cartItem.quantity -= 1
                cartItem.save()
                messages.info(request, 'Remove a book from already exist book')
        except cartItem.DoesNotExist:
            messages.info(request, 'Book not found')
    else:
        messages.info(request, 'You need to create your cart')


@login_required
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get_object_or_404(user=self.request.user)
        cartItems = CartItems.objects.filter(cart=cart)
        context = {
            'cart_items': cartItems
        }

class PaymentView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get_object_or_404(user=self.request.user)
        address = UserAddress.objects.get(user=self.request.user)
        if address.






