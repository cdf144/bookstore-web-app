from django.contrib import admin
from products.models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'category']
    search_fields = ['title', 'author']
    list_filter = ['category']

admin.site.register(Book, BookAdmin)
admin.site.register(Category)