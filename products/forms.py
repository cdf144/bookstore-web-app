from django import forms
import phonenumbers
from .models import UserPayment, User

"""class BookForms(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        labels = {
            'title' : 'Title',
            'author' : 'Author',
            'created_at' : 'Publication Date',
            'updated_at' : 'Republication Date',
            'price' : 'Price',
            'quantity' : 'Quantity',
            'summary' : 'Summary',
        }
        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput(),
            'created_at': forms.DateTimeInput(),
            'updated_at': forms.DateTimeInput(),
            'price': forms.ModelForm(),
            'quantity': forms.NumberInput(),
            'summary': forms.Textarea(),
        }
"""

PAYMENT_CHOICES = [
    ("CC", "Credit Card"),
    ("DC", "Debit Card"),
    ("PP", "PayPal"),
    ("CB", "Cash on Delivery"),
]


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(max_length=255)
    shipping_city = forms.CharField(max_length=255)
    shipping_country = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=255)
    mobile = forms.CharField(max_length=255)
    payment_method = forms.ChoiceField(choices=UserPayment.PAYMENT_CHOICES)

    def clean_mobile(self):
        mobile = str(self.cleaned_data.get("mobile"))
        try:
            mobile = phonenumbers.parse(mobile, "VN")
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Mobile number is invalid")
        if not phonenumbers.is_valid_number(mobile):
            raise forms.ValidationError("Mobile number is not a valid VN number")
        return mobile.national_number


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
