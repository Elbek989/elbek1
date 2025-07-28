from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=100)
    created_ad = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)
    context = models.TextField()

    def __str__(self):
        return self.title

class Autosalon(models.Model):
    title = models.CharField(max_length=255)
    context = models.TextField()
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.title

class Car(models.Model):
    model = models.CharField(max_length=100)
    price = models.IntegerField()
    year = models.DateField()
    color = models.CharField(max_length=100)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    salon = models.ForeignKey(Autosalon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model} - {self.year}"


# Create your models here.
