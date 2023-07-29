from django.db import models
from catastro.models import contribuyente

class historial_pagos(models.Model):
    contribuyente = models.ForeignKey(contribuyente,on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=40)
    subtotal_sin_des = models.FloatField()
    subtotal_años = models.FloatField()
    impuesto_adicional = models.FloatField()
    recargo = models.FloatField()
    multa = models.FloatField()
    aplica_descuento = models.CharField(max_length=15)
    descuento = models.FloatField(null=True)
    total = models.FloatField()
    estatus = models.CharField(max_length=15)
    autorizacion = models.CharField(max_length=20, null=True)
    cajero = models.CharField(max_length=20, null=True)

