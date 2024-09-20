from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm as DjangoPasswordResetForm
from .models import CustomUser, Property
from django.core.validators import FileExtensionValidator

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
        'required': 'required',
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': 'required',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'required',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'required': 'required',
            }),
        }

class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'required': 'required',
    }))

class PropertyForm(forms.ModelForm):
    # Feature-related fields
    security = forms.BooleanField(required=False)
    powerbackup = forms.BooleanField(required=False)
    wifi = forms.BooleanField(required=False)
    elevator = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    ac = forms.BooleanField(required=False)
    pool = forms.BooleanField(required=False)
    gym = forms.BooleanField(required=False)
    club = forms.BooleanField(required=False)

    images = forms.FileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    videos = forms.FileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])])    

    class Meta:
        model = Property
        fields = [ 
            'property_name','post_type', 'property_type1', 'specific_type1', 'specific_type2', 'maharera_number', 
            'property_price', 'property_area', 'bedrooms', 'balconies', 
            'bathrooms', 'status', 'ownership', 'city', 'locality', 'state', 
            'country', 'address', 'appartment', 'zip_code', 'landmark', 
            'security', 'powerbackup', 'wifi', 'elevator', 
            'parking', 'ac', 'pool', 'gym', 'club', 'images', 'videos','floor_plan'
        ]