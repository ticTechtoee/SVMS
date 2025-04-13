from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# accountApp/forms.py
from django import forms
from django.contrib.auth.models import User
from companyApp.models import Company
from accountApp.models import Employee

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )



# accountApp/forms.py
from django import forms
from django.contrib.auth.models import User
from companyApp.models import Company
from accountApp.models import Employee

class EmployeeCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[("admin", "Admin"), ("employee", "Employee")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})
    )

