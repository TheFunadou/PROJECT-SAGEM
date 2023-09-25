from django.db import models
from catastro.models import Datos_Contribuyentes


# MODELO IMPLEMENTADO ACTUAL
class historial_pagos(models.Model):
    folio = models.CharField(max_length=6)
    # Clave_Catastral contribuyente
    contribuyente =  models.ForeignKey(Datos_Contribuyentes,on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=40)
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
    fecha_hora= models.DateTimeField(auto_now_add=True)

#MODELOS EN FASE DE PRUEBA
class historial_adeudos(models.Model):
    ejercicio = models.CharField(max_length=4, primary_key=True)
    #Contribuyente
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    impuesto_predial = models.FloatField(default=0)
    impuesto_adicional = models.FloatField(default=0)
    multa = models.FloatField(default=0)
    recargo = models.FloatField(default=0)
    total = models.FloatField()
    estatus_descuento = models.CharField(max_length=20, default='NO SOLICITADO')
    descuento_multa = models.PositiveSmallIntegerField(default=0)
    descuento_recargo = models.PositiveSmallIntegerField(default=0)
    cajero = models.CharField(max_length=20, default='n/a')
    class Meta:
        unique_together = ('ejercicio', 'contribuyente',)
        
class historial_pago_predial(models.Model):
    folio = models.BigAutoField(primary_key=True)
    ejercicio_adeudo = models.ForeignKey(historial_adeudos, on_delete=models.CASCADE)
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    impuesto_predial = models.FloatField()
    impuesto_adicional = models.FloatField()
    recargo = models.FloatField(default=0)
    multa = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    cajero = models.CharField(max_length=20)
    total = models.FloatField()
    autorizacion = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('folio','ejercicio_adeudo','contribuyente',)
    