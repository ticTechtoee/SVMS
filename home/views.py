from django.shortcuts import render

def viewHome(request):
    return render(request, "home/HomeView.html")