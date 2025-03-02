from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
import random, string, json, copy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Factura
from .forms import FacturaForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            request.session["user_id"] = user.id
            return redirect("dashboard")
        else:
            error_message = "Usuario o contraseña incorrectos!"
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            User.objects.create(
                username=username, email=email, password=password, 
            )
            return redirect("login")
        else:
            error_message = "Las contraseñas no coinciden!"
            return render(request, "register.html", {"error_message": error_message})

    return render(request, "register.html")


def dashboard(request):
    id = request.session.get("user_id")
    if id is not None:
        try:
            data = User.objects.get(id=id)
            return render(request, "dashboard.html", {"data": data})
        except User.DoesNotExist:
            del request.session["user_id"]
    return redirect("login")


def logout(request):
    request.session.clear()
    return redirect("index")


def facturas(request):
    facturas = Factura.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            # No se requiere autenticación para guardar la factura
            factura.save()
            return redirect('facturas')
    else:
        form = FacturaForm()
    
    recomendaciones = obtener_recomendaciones(facturas)
    
    return render(request, 'facturas.html', {'facturas': facturas, 'form': form, 'recomendaciones': recomendaciones})

def obtener_recomendaciones(facturas):
    recomendaciones = []
    if len(facturas) > 1:
        consumo_actual = facturas[0].kwh
        consumo_anterior = facturas[1].kwh
        if consumo_actual > consumo_anterior:
            recomendaciones.append("Tu consumo ha aumentado respecto al mes pasado. Considera reducir el uso de energía.")
        else:
            recomendaciones.append("Buen trabajo! Tu consumo ha disminuido respecto al mes pasado.")
    return recomendaciones