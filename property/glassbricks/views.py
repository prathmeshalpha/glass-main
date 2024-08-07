import logging
from django.shortcuts import render


# Create your views here.
def home(request):
    
    return render(request,'layout.html')
    
def signup(request):
    
    return render(request,'signup.html')
