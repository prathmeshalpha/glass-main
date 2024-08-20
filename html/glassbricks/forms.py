from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm as DjangoPasswordResetForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,required=True)
    
    class Meta:
        model=CustomUser
        fields = ('username','email','password1','password2')
        
class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'required': 'required',
    }))