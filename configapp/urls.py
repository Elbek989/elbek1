from django.urls import path
from . import views
from .views import generate_car_pdf
urlpatterns = [
    path('', views.home, name='home'),
    path('salon/<int:pk>/', views.autosalon_detail, name='autosalon_detail'),
    path('salon/<int:pk>/cars/', views.autosalon_cars, name='autosalon_cars'),
    path('add-car/', views.add_car, name='add_car'),

    path('detail_car/<int:pk>/',views.detail_car,name = 'detail_car'),
    path('car/<int:car_id>/pdf/', generate_car_pdf, name='download_car_pdf'),
    path('download_car_pdf/<int:pk>/',views.download_car_pdf,name='download_car_pdf')
]
