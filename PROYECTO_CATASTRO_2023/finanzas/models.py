from django.db import models
from catastro.models import Datos_Contribuyentes


# MODELO IMPLEMENTADO ACTUAL
class historial_pagos(models.Model):
    folio = models.CharField(max_length=6,default='NP')
    # Clave_Catastral contribuyente
    contribuyente =  models.ForeignKey(Datos_Contribuyentes,on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=40, null=False)
    subtotal_años = models.FloatField(null=False)
    impuesto_adicional = models.FloatField(null=False)
    recargo = models.FloatField(default=0)
    descuento_recargo = models.PositiveSmallIntegerField(default=0)
    multa = models.FloatField(default=0)
    descuento_multa= models.PositiveSmallIntegerField(default=0)
    aplica_descuento = models.CharField(max_length=15, default='NO SOLICITADO')
    total = models.FloatField(null=False)
    estatus = models.CharField(max_length=15, default='NO PAGADO')
    autorizacion = models.CharField(max_length=20, null=True)
    cajero = models.CharField(max_length=20, null=False)
    fecha_hora= models.DateTimeField(auto_now_add=True)
 
class pago_predial(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    folio = models.BigIntegerField(default=0)
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=20, null=False)
    impuesto_predial = models.FloatField(null=False,default=0)
    impuesto_adicional = models.FloatField(null=False, default=0)
    recargo = models.FloatField(default=0)
    multa = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    estatus_descuento = models.CharField(max_length=15, default='NO SOLICITADO')
    cajero = models.CharField(max_length=20, default='N/A')
    estatus = models.CharField(max_length=20,default='NO PAGADO')
    total = models.FloatField(default=0)
    autorizacion = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()
    
