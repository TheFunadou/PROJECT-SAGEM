from django.db import models

# Create your models here.
class contribuyente(models.Model):
    rfc  = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ap = models.CharField(max_length=50)
    am = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, unique=True)
    activo = models.BooleanField(default=True)
    fecha_de_registro = models.DateTimeField(auto_now_add=True)

    def full_name_contribuyente(self):
        return self.nombre+' '+self.ap+' '+self.am

class datos_generales_predio(models.Model):
    clave_catastral = models.CharField(max_length=30)
    contribuyente = models.ForeignKey(contribuyente, on_delete=models.CASCADE)
    
    
    
    class Meta:
        unique_together = (('clave_catastral','contribuyente'),) 