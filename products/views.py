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

from .models import Book, Cart, CartItems, Order, OrderDetail, UserAddress, UserPayment, Category
from datetime import datetime
from .forms import CheckoutForm, PAYMENT_CHOICES


def users(request):
    """Displays a list of all users (for testing purposes)"""
    users = User.objects.all()
    template = loader.get_template("users.html")
    context = {"users": users}
    return HttpResponse(template.render(context, request))

def home(request):
    categories = Category.objects.all()
    random_books = Book.objects.order_by("?")[:12]  # Random 12 books
    return render(request, "home.html", {"categories": categories, "random_books": random_books})

def category_books(request, category_id):
    category = Category.objects.get(id=category_id)
    books = Book.objects.filter(category=category)
    
    paginator = Paginator(books, 12)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "category_books.html", {"category": category, "page_obj": page_obj})

"""
def book_list(request):
    # books = Book.objects.all()[:5]
    # books = Book.objects.get(id=10010)
    random_books = Book.objects.order_by("?").distinct()[:5]
    return render(request, "book_list.html", {"book_list": random_books})
"""

def book_list(request):
    categories = Category.objects.all().order_by('id')
    for category in categories:
        category.random_books = category.book_set.order_by('?')[:4]  # Get 4 random books for each category

    paginator = Paginator(categories, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'book_list.html', context)

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


"""
def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart = Cart.objects.get(created_by=request.user)
    try:
        cartItem = CartItems.objects.get(cart=cart, book=book)
        if cartItem.quantity == 0:
            cartItem.delete()
            messages.info(request, "Item deleted successfully")
        else:
            cartItem.quantity -= 1
            cartItem.save()
            messages.info(request, "Item removed successfully")
    except CartItems.DoesNotExist:
        messages.info(request, 'You do not have the product in cart')

"""

def remove_from_cart(request, book_title):
    book = get_object_or_404(Book, title=book_title)
    try:
        cart = Cart.objects.get(created_by=request.user)
        cart_item = CartItems.objects.get(cart=cart, book=book)
        cart_item.delete()
        messages.info(request, "Book removed from your cart")
    except Cart.DoesNotExist:
        messages.error(request, "You do not have a cart")
    except CartItems.DoesNotExist:
        messages.error(request, "Book is not in your cart")
    return redirect("order-summary")


class CartView(View):
    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, created_by=self.request.user)
        cartItems = CartItems.objects.filter(cart=cart)
        totalPrice = 0
        for item in cartItems:
            book = Book.objects.get(title=item.book.title)
            totalPrice += item.quantity * book.price
        context = {"cart_items": cartItems, "orders": cart, "total_price": totalPrice}
        return render(self.request, "cart.html", context)


"""
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user).first()
        if order.address:
            context = {
                'order': order
            }
            return render(self.request, 'payment.html')
        else:
            messages.info('You do not have an billing address yet')
            return redirect('checkout')
"""


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

@login_required
def profile(request):
    """Displays the user's profile"""
    user = request.user

    # Deduplicate addresses
    unique_addresses = []
    seen_addresses = set()
    for address in user.useraddress_set.all():
        identifier = (address.address_line, address.city, address.postal_code, address.country, address.mobile)
        if identifier not in seen_addresses:
            unique_addresses.append(address)
            seen_addresses.add(identifier)

    # Deduplicate payment methods
    unique_payments = []
    seen_payments = set()
    for payment in user.userpayment_set.all():
        identifier = (payment.payment_type, payment.expiry_date)
        if identifier not in seen_payments:
            unique_payments.append(payment)
            seen_payments.add(identifier)

    context = {
        'user': user,
        'addresses': unique_addresses,
        'payments': unique_payments,
    }

    return render(request, 'profile.html', context)
