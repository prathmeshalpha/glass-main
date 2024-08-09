from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,required=True)
    
    class Meta:
        model=CustomUser
        fields = ('username','email','password1','password2')