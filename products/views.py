
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from models import CartItems, Cart, UserAddress, Category, Book
from datetime import datetime
import stripe

# Create your views here.
@login_required
def add_to_cart(request, book, user):
    try:
        cart = Cart.objects.get(book=book, user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
    try:
        cartItem = CartItems.objects.get(cart=cart)
        cartItem.quantity += 1
        cartItem.save()
        messages.info(request, "You have successfully added the item")
    except CartItems.DoesNotExist:
        cartItem = cartItem.objects.create(cart=cart, book=book, quantity=1)
        cartItem.save()
        messages.info(request, "You have created your cart")

@login_required
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user)
            cartItems = CartItems.objects.filter(cart=cart)
            context = {
                'Books': cartItems
            }
            return render(self.request,'products/order_summary.html', context)
        except Cart.DoesNotExist:
            messages.warning('You do not have any cart or cart items')

class PaymentView(View):
    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)
        try:
            userAddress = UserAddress.objects.get(user=self.request.user)
            context = {
                'Order' : cart
            }
        except UserAddress.DoesNotExist:
            messages.warning( 'You do not have a user address')



class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user)
            userAddress = UserAddress.objects.get(user=self.request.user)

        except UserAddress.DoesNotExist:
            messages.warning( '')
        except Cart.DoesNotExist:
            messages.warning('')

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(name=self.kwargs['name'])
        books = Book.objects.filter(category=category)
        context = {
            'Category' = category,

        }














