from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Book


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
