# myapp/forms.py

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control rounded-0',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-0',
            'autofocus': True,
            'placeholder': 'Enter your username'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-0',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-0',
            'placeholder': 'Confirm your password'
        })
    )
    notifications = forms.BooleanField(
        required=False,
        initial=False,
        label='Receive notifications',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input rounded-0'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'notifications')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-0',
            'autofocus': True,
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-0',
            'placeholder': 'Enter your password'
        })
    )



class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
