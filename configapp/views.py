import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .models import Autosalon, Car,Brand
from .forms import BrandForm, AutosalonForm, CarForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
from io import BytesIO
def generate_car_pdf(request, car_id):
    car = Car.objects.get(id=car_id)


    qr_data = f"Mashina nomi: {car.model}, ID: {car.id}"
    qr_img = qrcode.make(qr_data)
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)

    template = get_template("car_pdf_template.html")
    html = template.render({
        'car': car,
        'qr_code': qr_io
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="car_{car.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    return response
def detail_car(request,pk):
    car = get_object_or_404(Car,id = pk)
    site_url = f"http://{request.get_host()}/"
    context = {
        'car':car,
        'site_url':site_url
    }
    return render(request,'car_detail.html',context=context)

def home(request):
    salons = Autosalon.objects.all()
    brands = Brand.objects.all()
    cars = Car.objects.all()

    return render(request, 'home.html', {
        'salons': salons,
        'brands': brands,
        'cars': cars,
    })

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
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})
def download_car_pdf(request, pk):
    car = Car.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{car.model}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4

    # 🔹 Mashina nomi
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, page_height - 50, car.model)

    # 🔹 Year, Price, Create Date
    c.setFont("Helvetica", 14)
    c.drawString(50, page_height - 100, f"Year: {car.year}")
    c.drawString(50, page_height - 130, f"Price: {car.price}")



    # 🔹 Web sayt manziliga QR kod
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
# Create your views here.
