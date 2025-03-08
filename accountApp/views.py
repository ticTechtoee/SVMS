from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('home:HomeView')  # Redirect to homepage
    else:
        form = SignupForm()
    return render(request, 'accountApp/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:HomeView')  # Redirect to homepage
    else:
        form = LoginForm()
    return render(request, 'accountApp/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('accountApp:login')  # Redirect to login page after logout
