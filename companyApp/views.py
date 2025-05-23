from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CompanyForm
from django.contrib.auth.decorators import login_required

@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboardApp:admin_dashboard')
    else:
        form = CompanyForm()

    return render(request, 'companyApp/create_company.html', {'form': form})
