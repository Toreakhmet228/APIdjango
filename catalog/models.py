from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sort = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    COLORS = [
        ('RED', 'Red'),
        ('GREEN', 'Green'),
        ('BLUE', 'Blue'),
        # добавьте больше цветов при необходимости
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    color = models.CharField(max_length=50, choices=COLORS)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Review(models.Model):
    body = models.TextField()
    rate = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review for {self.product.title} by {self.user.username}'
