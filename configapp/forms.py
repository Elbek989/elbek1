from django import forms
from .models import Brand, Autosalon, Car

# 🔹 Brand uchun forma
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'context']

# 🔹 Autosalon uchun forma
class AutosalonForm(forms.ModelForm):
    class Meta:
        model = Autosalon
        fields = ['title', 'context', 'email', 'phone', 'adress', 'image']

# 🔹 Car uchun forma
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'price', 'year', 'color', 'brand', 'salon']

        widgets = {
            'year': forms.DateInput(attrs={'type': 'date'}),
        }
