from django.db import models
from django.contrib.auth.models import User

#For time based tracking
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    picture_link = models.TextField(default='')
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))  # Default to 30 days from now
    
    def __str__(self):
        return self.name
    
    def is_active(self): #To determine whether the auction is still active
        return self.end_date > timezone.now()


class Bid(models.Model):
    product = models.ForeignKey(Product, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.product.name}"