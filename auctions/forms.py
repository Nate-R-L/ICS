from django import forms
from .models import Bid, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'current_bid', 'end_date']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

#Class to allow for custom user signup HTML
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose your username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter a secure password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}),
        }
        # This will remove help texts for all fields
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'usable_password':None,
        }

    # Delete the authentifcation poppup & force to enable
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
