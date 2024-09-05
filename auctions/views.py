from django.shortcuts import render, redirect
from .models import Product, Bid
from .forms import BidForm
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = Product.objects.all()

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
