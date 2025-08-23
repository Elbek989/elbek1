from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Brand, Autosalon, Car


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'context']

class AutosalonForm(forms.ModelForm):
    class Meta:
        model = Autosalon
        fields = ['title', 'context', 'email', 'phone', 'adress', 'image']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'price', 'year', 'color', 'brand', 'salon']

        widgets = {
            'year': forms.DateInput(attrs={'type': 'date'}),
        }
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'context']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))