from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario, SolicitudServicio, Factura
from django.forms.widgets import HiddenInput
from datetime import datetime

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['idprod', 'nomprod', 'descprod', 'precio', 'imagen']

class IniciarSesionForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=20, required=True, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", initial='Cliente', widget=forms.HiddenInput())
    dirusu = forms.CharField(max_length=300, required=True, label="Dirección")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'tipousu', 'rut', 'dirusu']

class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=20, required=False, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", widget=forms.HiddenInput())
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección")

    class Meta:
        fields = '__all__'
        
class SolicitudServicioForm(forms.Form):
    TIPOSOL_CHOICES = [
        ('Mantención', 'Mantención'),
        ('Reparación', 'Reparación'),
    ]
    tiposol = forms.ChoiceField(choices=TIPOSOL_CHOICES)
    fechavisita = forms.DateField(widget=forms.SelectDateWidget())
    descsol = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'fechavisita' in initial:
            initial['fechavisita'] = initial['fechavisita'].isoformat()
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean_fechavisita(self):
        fechavisita = self.cleaned_data['fechavisita']
        return fechavisita