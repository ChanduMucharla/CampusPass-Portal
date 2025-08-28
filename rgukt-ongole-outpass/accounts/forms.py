
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    id_number = forms.CharField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    year_of_study = forms.CharField(required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username','full_name','phone','email','id_number','role','year_of_study','profile_photo','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
