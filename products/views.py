import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book, Cart, CartItems, Order, OrderDetail, UserAddress, UserPayment, WishList
from datetime import datetime
from .forms import CheckoutForm, PAYMENT_CHOICES, UserInformation


def users(request):
    """Displays a list of all users (for testing purposes)"""
    users = User.objects.all()
    template = loader.get_template("users.html")
    context = {"users": users}
    return HttpResponse(template.render(context, request))


def book_list(request):
    """Displays a list of 5 random books at the main page for book."""
    # books = Book.objects.all()[:5]
    # books = Book.objects.get(id=10010)
    random_books = Book.objects.order_by("?").distinct()[:5]
    return render(request, "book_list.html", {"book_list": random_books})


def book_detail(request, id):
    """Displays book details"""
    book = get_object_or_404(Book, id=id)
    return render(request, "book_detail.html", {"book": book})


def search(request):
    """Searches for books by title or author"""
    query = request.GET.get("q")
    search_results = []

    if query:
        search_results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

        paginator = Paginator(search_results, 10)  # Show 10 results per page
        page_number = request.GET.get("page")
        try:
            search_results = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            search_results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            search_results = paginator.get_page(paginator.num_pages)

    return render(request, "search.html", {"search_results": search_results})


@login_required
def add_to_cart(request, book_title):
    """Adds book to cart"""
    user = User.objects.get(id=request.user.id)
    if user == None:
        return redirect("")
    book = Book.objects.get(title=book_title)
    try:
        cart = Cart.objects.get(created_by=request.user)
        try:
            cartItem = CartItems.objects.get(cart=cart, book=book)
            cartItem.quantity += 1
            cartItem.save()
            return HttpResponse("You have successfully")
        except CartItems.DoesNotExist:
            cartItem = CartItems.objects.create(cart=cart, book=book, quantity=1)
            cartItem.save()
            return HttpResponse("Book added to your cart")
    except Cart.DoesNotExist:
        timeNow = datetime.now()
        cart = Cart.objects.create(created_by=request.user, created_at=timeNow)
        cartItem = CartItems.objects.create(cart=cart, book=book, quantity=1)
        cartItem.save()
        return HttpResponse("Your cart have been added")




class CartDetailView(View):
    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, created_by=self.request.user)
        cartItems = CartItems.objects.filter(cart=cart)
        totalPrice = 0
        for item in cartItems:
            book = Book.objects.get(title=item.book.title)
            totalPrice += item.quantity * book.price
        context = {"cart_items": cartItems, "orders": cart, "total_price": totalPrice}
        return render(self.request, "cart-detail.html", context)
    def post(self, *args, **kwargs):
        cart = get_object_or_404(Cart, created_by=self)
        book_name = self.request.POST.get("book_name")
        action = self.request.POST.get("action")
        if book_name and action:
            book = CartItems.objects.get(cart=cart, name=book_name)
            if action == "increment":
                book.quantity += 1
                book.save()
            if action == "decrement":
                if book.quantity > 1:
                    book.quantity -= 1
                    book.save()
                else:
                    book.delete()
        return redirect("cart-detail")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(created_by=self.request.user)
            form = CheckoutForm()
            context = {"Form": form, "Order": cart, "PAYMENT_CHOICES": PAYMENT_CHOICES}
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            return HttpResponse("You do not have a cart")


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data.get("shipping_address")
            city = form.cleaned_data.get("shipping_city")
            country = form.cleaned_data.get("shipping_country")
            postal_code = form.cleaned_data.get("postal_code")
            mobile = form.cleaned_data.get("mobile")
            payment_method = form.cleaned_data.get("payment_method")
            expiry_date = datetime.now()  # leave as random for now
            user_payment = UserPayment.objects.create(
                user=self.request.user,
                payment_type=payment_method,
                expiry_date=expiry_date,
            )
            user_payment.save()
            shipping_info = UserAddress.objects.create(
                user=self.request.user,
                address_line=shipping_address,
                city=city,
                country=country,
                postal_code=postal_code,
                mobile=mobile,
            )
            shipping_info.save()
            order = Order.objects.create(
                user=self.request.user,
                status=Order.STATUS_CHOICES[0][0],
                address=shipping_info,
                order_date=datetime.now(),
            )
            order.save()
            cart = Cart.objects.get(created_by=self.request.user)
            cartItems = CartItems.objects.filter(cart=cart)
            for cartItem in cartItems:
                orderDetail = OrderDetail.objects.create(
                    order=order, book=cartItem.book, quantity=cartItem.quantity
                )
                orderDetail.save()
                cartItem.delete()
            return redirect("book_list")
        else:
            messages.info(
                request=self.request,
                message="You have not filled all the needed information",
            )
            return redirect("check_out")

def add_to_wishlist(request, title):
    book = WishList.objects.get(title=title)
    if book is not None:
        return
    favoriteBook = WishList.objects.create(title=title, user=request.user)
    favoriteBook.save()
    return redirect("book_detail")

def remove_from_wishlist(request, title):
    try:
        bookToRemove = WishList.objects.get(title=title)
        bookToRemove.delete()
        return redirect("")
    except WishList.DoesNotExist:
        return HttpResponse(status=404)
def get_user_wishlist(request):
    wishlistBook = WishList.objects.filter(user=request.user)
    context = {
        "wishlistBook" : wishlistBook
    }

    return render(request, "", context,)

class AccountManagementView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        form = UserInformation(instance=self.request.user)
        context = {
            'user': self.request.user,
            'edit': form
        }
        return render(self.request, "user-information.html", context)
    def post(self, *args, **kwargs):
        form = UserInformation(self.request.POST or None)
        if form.has_changed() and form.is_valid():
            form = User(self.request.POST, instance=self.request.user)
            form.save()
        return redirect("")
