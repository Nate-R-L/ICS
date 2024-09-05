from django.urls import path
from .views import product_list

urlpatterns = [
    path('', product_list, name='product_list'),  # Maps the root URL of the app to the product_list view
]
