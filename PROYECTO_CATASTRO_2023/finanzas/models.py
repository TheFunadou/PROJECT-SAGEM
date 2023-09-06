from django.db import models
from catastro.models import Datos_Contribuyentes
from catastro.models import Datos_gen_predio

class historial_pagos(models.Model):
    folio = models.CharField(max_length=6)
    # Clave_Catastral contribuyente
    contribuyente =  models.ForeignKey(Datos_Contribuyentes,on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=40)
    subtotal_sin_des = models.FloatField()
    subtotal_años = models.FloatField()
    impuesto_adicional = models.FloatField()
    recargo = models.FloatField()
    descuento_recargo = models.PositiveSmallIntegerField(default=0)
    multa = models.FloatField()
    descuento_multa= models.PositiveSmallIntegerField(default=0)
    aplica_descuento = models.CharField(max_length=15)
    total = models.FloatField()
    estatus = models.CharField(max_length=15)
    autorizacion = models.CharField(max_length=20, null=True)
    cajero = models.CharField(max_length=20, null=False)
    # fecha_hora= models.DateTimeField(auto_now_add=True)
