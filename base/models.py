from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import random


class User(models.Model):

    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=80, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

class Factura(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Hacer el campo opcional
    fecha = models.DateField(auto_now_add=True)
    kwh = models.FloatField()
    valor = models.FloatField(default=0.0)  # Valor predeterminado
    mes = models.IntegerField(default=1)  # Valor predeterminado para el mes
    año = models.IntegerField(default=2025)  # Valor predeterminado para el año

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonimo'} - {self.fecha} - {self.kwh} kWh - ${self.valor} - {self.mes}/{self.año}"