from django.contrib import admin
from .models import Product, Bid

class ProductAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('name', 'starting_bid', 'current_bid', 'highest_bid', 'end_date', 'picture_link')

    # Make highest_bid a read-only field in the edit view
    readonly_fields = ('highest_bid',)

    # Customize form view (optional)
    fields = ('name', 'description', 'starting_bid', 'current_bid', 'highest_bid', 'end_date', 'picture_link')

admin.site.register(Product, ProductAdmin)
admin.site.register(Bid)


#from django.contrib import admin

# Register your models here.
#from .models import Product

#admin.site.register(Product)
