from django.db import models
from catastro.models import Datos_Contribuyentes
 
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


class model_pago_predial(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    folio = models.BigIntegerField(default=0)
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=20, null=False)
    impuesto_predial = models.DecimalField(max_digits=13, decimal_places=2, default=0, null=False)
    impuesto_adicional = models.DecimalField(max_digits=13, decimal_places=2, default=0, null=False)
    recargo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    multa = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    estatus_descuento = models.CharField(max_length=15, default='NO SOLICITADO')
    cajero = models.CharField(max_length=20, default='N/A')
    estatus = models.CharField(max_length=20,default='NO PAGADO')
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    autorizacion = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()


class pago_predial_solicitud_descuento(models.Model):
    id = models.BigAutoField(primary_key=True ,null=False)
    id_registro_pago = models.ForeignKey(model_pago_predial, on_delete=models.CASCADE)
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    porcentaje_recargo = models.IntegerField()
    recargo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    porcentaje_multa = models.IntegerField()
    multa = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    
    