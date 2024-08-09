import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.urls import reverse


# Create your views here.
def home(request):
    
    return render(request,'index.html')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            # Log or print form errors
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    

def signin(request):
        if request.method =='POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username =  form.cleaned_data.get('username')
                password =  form.cleaned_data.get('password')
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    form.add_error(None,'Invalid username or password')
            else:
                print(form.errors)
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
            
def logout(request):
    logout(request)
    return redirect('signin.html')

