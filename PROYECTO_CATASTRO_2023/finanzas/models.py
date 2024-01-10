from django.db import models
from catastro.models import Datos_Contribuyentes
 
class pagos(models.Model):
    #UNIQUE
    id = models.BigAutoField(primary_key=True, null=False)
    #pk
    folio = models.BigIntegerField(default=0)
    contribuyente = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=20, null=False)
    #IMPUESTO PREDIAL
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, default=0, null=False)
    impuesto_adicional = models.DecimalField(max_digits=13, decimal_places=2, default=0, null=False)
    recargo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    desc_recargo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    multa = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    desc_multa = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    estatus_descuento = models.CharField(max_length=15, default='NO SOLICITADO')
    cajero = models.CharField(max_length=20, default='N/A')
    estatus = models.CharField(max_length=20,default='NO PAGADO')
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    autorizacion = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()


class tabla_derechos(models.Model):
    id_derecho  = models.PositiveSmallIntegerField(null=False)
    categoria = models.CharField(max_length=200, null=False)
    nombre_derecho = models.CharField(max_length=200, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class detalle_pago_derecho(models.Model):
    id_pago = models.ForeignKey(pagos, on_delete = models.CASCADE)
    id_derecho = models.ForeignKey(tabla_derechos, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200, null=True)
    
    
    
    



    