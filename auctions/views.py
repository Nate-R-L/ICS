from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Bid
from .forms import BidForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from decimal import Decimal
from django.db.models import Max
from django.utils.timezone import now
from .forms import EditUserForm

### PRODUCT LIST VIEW ###
@login_required
def product_list(request):
    # Handle filtering based on GET parameters
    filter_type = request.GET.get('filter', 'all')  # Default to showing all products

    if filter_type == 'ongoing':
        products = Product.objects.filter(end_date__gt=timezone.now())  # Ongoing auctions
    elif filter_type == 'ended':
        products = Product.objects.filter(end_date__lte=timezone.now())  # Ended auctions
    else:
        products = Product.objects.all()  # Show all auctions

    if request.method == 'POST':
        form = BidForm(request.POST)
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        if form.is_valid():
            bid_amount = form.cleaned_data['amount']
            # Use the current bid if it exists, otherwise use the starting bid
            current_highest_bid = product.current_bid if product.current_bid > 0 else product.starting_bid

            # Ensure the bid is higher than the current bid or starting bid
            if bid_amount > current_highest_bid:
                bid = form.save(commit=False)
                bid.product = product
                bid.user = request.user
                bid.save()

                # Update the product's current bid
                product.current_bid = bid_amount
                product.save()

                return redirect('product_list')
            else:
                # Render the template with an error message if the bid is too low
                return render(request, 'auctions/product_list.html', {
                    'products': products,
                    'form': form,
                    'error_message': 'Your bid must be higher than the current bid or starting bid.'
                })
        else:
            # Handle invalid form case
            return render(request, 'auctions/product_list.html', {
                'products': products,
                'form': form,
                'error_message': 'Invalid bid input.'
            })

    else:
        # If it's a GET request, just display the product list and form
        form = BidForm()
        return render(request, 'auctions/product_list.html', {'products': products, 'form': form})

def product_detail(request, product_id):
    # Fetch the specific product (coin) by its ID
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'auctions/product_detail.html', {'product': product})

### PLACE BID VIEW - REQUIRED LOGIN
@login_required
def place_bid(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the auction is still active
    if product.end_date <= timezone.now():
        return HttpResponseForbidden("This auction has ended. No further bids are allowed.")

    if request.method == 'POST':
        bid_amount = Decimal(request.POST.get('amount'))  # Use Decimal for monetary values
        current_bid = product.current_bid if product.current_bid > 0 else product.starting_bid

        if bid_amount > current_bid:
            # Create and save the new bid
            new_bid = Bid.objects.create(product=product, user=request.user, amount=bid_amount)
            product.current_bid = bid_amount
            product.save()

            return redirect('product_list')
        else:
            # Pass the error message specific to the product that received the lower bid
            products = Product.objects.all()
            error_message = {product.id: "Your bid must be higher than the current bid or starting bid."}
            return render(request, 'auctions/product_list.html', {
                'products': products,
                'error_message': error_message
            })
        
### SIGNUP VIEW
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Redirect after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

### ACCOUNT VIEW
@login_required
def account_view(request):
    user = request.user

    # Get the most recent bid for each product by the logged-in user
    user_bids = Bid.objects.filter(user=user).values('product').annotate(latest_bid=Max('id'))

    # Fetch the actual bid objects for those latest bids
    recent_bids = Bid.objects.filter(id__in=[bid['latest_bid'] for bid in user_bids]).select_related('product')

    # Determine auction status and outcome
    for bid in recent_bids:
        product = bid.product
        bid.max_bid = Bid.objects.filter(product=product).aggregate(Max('amount'))['amount__max']
        bid.is_winning = bid.amount == bid.max_bid
        bid.auction_ended = product.end_date <= now()  # Check if the auction has ended

        # Determine result: "won" or "lost"
        if bid.auction_ended:
            bid.result = "won" if bid.is_winning else "lost"
        else:
            bid.result = None  # Auction is still ongoing

    return render(request, 'auctions/account.html', {'recent_bids': recent_bids})

@login_required
def edit_user_info(request):
    user = request.user

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')  # Redirect back to the profile page
    else:
        form = EditUserForm(instance=user)

    return render(request, 'auctions/edit_user_info.html', {'form': form})