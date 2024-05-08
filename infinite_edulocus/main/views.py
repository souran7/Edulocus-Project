from django.shortcuts import render
from django.db.models import Max
from django.core.paginator import Paginator
from django.template.defaulttags import register
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from .forms import  LoginForm

from edulocus.settings import LOGIN_URL





def login_auth(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home page if user is already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        provided_password = request.POST.get('password')
        default_password = "Password" # Replace with your actual default password

        # Attempt to authenticate with the provided password
        user = authenticate(request, username=username, password=provided_password)

        # If authentication with the provided password fails, try the default password
        if user is None and provided_password == default_password:
            try:
                user = User.objects.get(username=username)
                # Log in the user without calling authenticate (use with caution)
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            except User.DoesNotExist:
                pass

        if user is not None:
            # Authentication with the provided password succeeded
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login

        # Authentication failed with both the provided and default passwords
        messages.error(request, 'Username or Password Incorrect')
        return redirect('login')

    return render(request, 'login.html', context={'login_form': LoginForm(request.POST)})

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required(login_url=LOGIN_URL)
def home(request):
    return render(request, 'home.html')


def landing_page(request):
    return render(request, 'index.html')