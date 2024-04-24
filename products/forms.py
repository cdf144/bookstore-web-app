from django import forms
from models import Book
from models import UserAddress
from cities_light.forms import CityForm

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

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(require=True)
    billing_address = forms.CharField(require=True)
    shipping_city = CityForm()