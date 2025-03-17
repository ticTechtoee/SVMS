from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def viewUserDetail(request):
    users = User.objects.all()  # Fetch all registered users
    return render(request, "home/UserDetailView.html", {"users": users})


def viewHome(request):
    return render(request, "home/HomeView.html")

