from django.urls import path
from django.contrib.auth import views as auth_views
from .views import product_list, signup, place_bid, account_view
from . import views

urlpatterns = [
    path('', product_list, name='product_list'),  # Maps the root URL of the app to the product_list view
    path('place-bid/<int:product_id>/', place_bid, name='place_bid'),  # URL for placing a bid
    path('account/', account_view, name='account'),

    # URL for the product detail page
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # If wanting to place a bid
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', signup, name='signup'),

    #URL for editing profile data
    path('account/edit-user/', views.edit_user_info, name='edit_user_info'),
    
]