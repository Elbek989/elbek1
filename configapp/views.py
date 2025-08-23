import os
import base64
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from xhtml2pdf import pisa
import qrcode

from .models import Autosalon, Car, Brand
from .forms import BrandForm, AutosalonForm, CarForm, LoginForm


# 🔹 Custom decorator for unauthenticated users
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# 🔹 Home page
def home(request):
    salons = Autosalon.objects.all()
    brands = Brand.objects.all()
    cars = Car.objects.all()
    return render(request, 'home.html', {
        'salons': salons,
        'brands': brands,
        'cars': cars,
    })


# 🔹 Car detail view
def detail_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    site_url = f"http://{request.get_host()}/"
    context = {
        'car': car,
        'site_url': site_url
    }
    return render(request, 'car_detail.html', context)


# 🔹 Autosalon detail view
def autosalon_detail(request, pk):
    salon = get_object_or_404(Autosalon, pk=pk)
    return render(request, 'autosalon_detail.html', {'salon': salon})


# 🔹 Autosalon's car list
def autosalon_cars(request, pk):
    salon = get_object_or_404(Autosalon, pk=pk)
    cars = Car.objects.filter(salon=salon)
    return render(request, 'autosalon_cars.html', {'salon': salon, 'cars': cars})


# 🔹 Add car
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')  # Make sure 'car_list' exists in urls.py
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


# 🔹 Generate car PDF with HTML template and QR
def generate_car_pdf(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    qr_data = f"Mashina nomi: {car.model}, ID: {car.id}"
    qr_img = qrcode.make(qr_data)
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)

    qr_base64 = base64.b64encode(qr_io.getvalue()).decode('utf-8')

    template = get_template("car_pdf_template.html")
    html = template.render({
        'car': car,
        'qr_code': qr_base64
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="car_{car.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    return response


# 🔹 Download car PDF using ReportLab
def download_car_pdf(request, pk):
    car = get_object_or_404(Car, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{car.model}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4

    # Car name
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, page_height - 50, car.model)

    # Year, Price
    c.setFont("Helvetica", 14)
    c.drawString(50, page_height - 100, f"Year: {car.year}")
    c.drawString(50, page_height - 130, f"Price: {car.price}")

    # QR code to website
    site_url = f"http://{request.get_host()}/"
    qr_img = qrcode.make(site_url)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_reader = ImageReader(buffer)

    c.drawImage(qr_reader, page_width - 200, 50, width=120, height=120)

    c.showPage()
    c.save()
    return response


# 🔹 Login view
@unauthenticated_user
def loginPage(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Username yoki parol xato!")

    return render(request, "login.html", {"form": form})
