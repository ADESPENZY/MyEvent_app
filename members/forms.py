from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your email'
        })
    )
    
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your last name'
        })
    )
    
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Choose a username'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter a password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Re-enter your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
