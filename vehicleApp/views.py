from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import VehicleForm

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:HomeView')
    else:
        form = VehicleForm()

    return render(request, 'vehicleApp/create_vehicle.html', {'form': form})
