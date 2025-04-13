from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
# accountApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, EmployeeCreationForm
from accountApp.models import Employee
from django.contrib.auth.decorators import login_required, user_passes_test
import random
import string

# accountApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, EmployeeCreationForm
from accountApp.models import Employee
import random
import string

from django.db import IntegrityError
from django.contrib import messages  # Optional: for user feedback

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



def generate_random_password(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



@login_required
def create_employee_view(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            company = form.cleaned_data['company']

            random_password = generate_random_password()

            try:
                user = User.objects.create_user(
                    username=username, email=email, password=random_password
                )
                Employee.objects.create(user=user, company=company, role=role)

                # Render HTML content from template
                subject = "Your Employee Account Details"
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [email]

                html_content = render_to_string('accountApp/emails/employee_welcome.html', {
                    'username': username,
                    'password': random_password,
                    'company': company.name
                })

                text_content = f"Username: {username}\nPassword: {random_password}"

                email_msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send()

                messages.success(request, f"Employee created and email sent to {email}.")
                return redirect('home:HomeView')

            except IntegrityError:
                form.add_error('username', 'This username is already taken. Please choose a different one.')
    else:
        form = EmployeeCreationForm()

    return render(request, 'accountApp/create_employee.html', {'form': form})

