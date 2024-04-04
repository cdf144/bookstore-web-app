from django.db import models
from django.contrib.auth.models import User

PAYMENT_CHOICES = {
    ("CC", "Credit Card"),
    ("DC", "Debit Card"),
    ("PP", "PayPal"),
    ("CB", "Cash on Delivery"),
}

# Create your models here.
class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_CHOICES, max_length=2)
    expiry_date = models.DateField(null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user_id', 'payment_type'], name='user_payment'
    #         )
    #     ]


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user_id', 'address_line'], name='user_address'
    #         )
    #     ]


class Cart(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    summary = models.CharField(max_length=255)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['cart_id', 'book_id'], name='book_cart'
    #         )
    #     ]

