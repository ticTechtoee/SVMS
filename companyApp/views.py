from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CompanyForm

def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:HomeView')
    else:
        form = CompanyForm()

    return render(request, 'companyApp/create_company.html', {'form': form})
