from django.shortcuts import render
from .models import Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'auctions/product_list.html', {'products': products})
