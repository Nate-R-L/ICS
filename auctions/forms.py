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
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','email')
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

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)  # Create the user object but don't save it yet
        user.email = self.cleaned_data['email']  # Assign the cleaned email field to the user
        if commit:
            user.save()  # Save the user if commit is True
        return user  # Return the user object


    # Delete the authentifcation poppup & force to enable
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

#Edit user metadata in account page
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Fields the user can edit