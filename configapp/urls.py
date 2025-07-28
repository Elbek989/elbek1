from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('salon/<int:pk>/', views.autosalon_detail, name='autosalon_detail'),
    path('salon/<int:pk>/cars/', views.autosalon_cars, name='autosalon_cars'),
]
