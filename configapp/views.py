from django.shortcuts import render, get_object_or_404
from .models import Autosalon, Car,Brand
from .forms import BrandForm, AutosalonForm, CarForm


def home(request):
    brands = Brand.objects.all()
    salons = Autosalon.objects.all()
    context = {
        'brands': brands,
        'salons': salons,
    }
    return render(request, 'home.html', context)


def autosalon_detail(request, pk):
    salon = get_object_or_404(Autosalon, pk=pk)
    return render(request, 'autosalon_detail.html', {'salon': salon})

def autosalon_cars(request, pk):
    salon = get_object_or_404(Autosalon, pk=pk)
    cars = Car.objects.filter(salon=salon)
    return render(request, 'autosalon_cars.html', {'salon': salon, 'cars': cars})
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})

# Create your views here.
