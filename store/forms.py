from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.Form):
    address = forms.CharField(
        label="Delivery address",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "House number, street, city, PIN code"})
    )
