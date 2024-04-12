from django import forms
from models import Book

class BookForms(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        labels = {
            'title' : 'Title',
            'author' : 'Author',
            'created_at' : 'Publication Date',
            'updated_at' : 'Republication Date',
            'publisher' : 'Publisher',
            'price' : 'Price',
            'quantity' : 'Quantity',
            'summary' : 'Summary',
        }
        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput(),
            'created_at': forms.DateTimeInput(),
            'updated_at': forms.DateTimeInput(),
            'publisher' : forms.TextInput(),
            'price': forms.ModelForm(),
            'quantity': forms.NumberInput(),
            'summary': forms.Textarea(),
        }

