import random

from django.contrib.auth.models import User
from django.db import models


class UserPayment(models.Model):
    PAYMENT_CHOICES = [
        ("CC", "Credit Card"),
        ("DC", "Debit Card"),
        ("PP", "PayPal"),
        ("CB", "Cash on Delivery"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_CHOICES, max_length=2)
    expiry_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_type}"

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

    def __str__(self):
        return f"{self.user.username} - {self.address_line}"

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
    description = models.TextField(default="No description provided")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    summary = models.TextField(default="No description provided")
    img_path = models.CharField(max_length=255, default=None, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # if the book is new, then randomize its quantity
            self.quantity = random.randint(10, 30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.author}"


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['cart_id', 'book_id'], name='book_cart'
    #         )
    #     ]


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    shipped_date = models.DateField(null=True)
    order_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.status}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.book} - {self.quantity}"
