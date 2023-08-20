from django.db import models

# Create your models here.

class Datos_Contribuyentes(models.Model):

    #Inicializacion de los atributos del modelo Datos_Contribuyentes

    clave_catastral = models.CharField(primary_key=True,max_length=50)
    rfc = models.CharField(max_length=13)
    tramite = models.CharField(max_length=60)
    nombre = models.CharField(max_length=25)
    apaterno = models.CharField(max_length=25)
    amaterno = models.CharField(max_length=25)
    telefono = models.CharField(max_length=10)
    tipo = models.CharField(max_length=7)
    calle = models.CharField(max_length=35)
    num_int = models.CharField(max_length=5)
    num_ext = models.CharField(max_length=5)
    colonia_fraccionamiento = models.CharField(max_length=55)
    localidad = models.CharField(max_length=55)
    codigo_postal = models.CharField(max_length=10)
    
    class Meta:
         unique_together = ('clave_catastral', 'rfc',)
         
    
class Datos_inmuebles(models.Model):

     #Inicializacion de los atributos del modelo Datos del inmueble
     id_inmueble = models.AutoField(primary_key=True)
     fk_clave_catastral = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
     pk_estado_fisico_predio = models.CharField(max_length=40)
     tipo_predio = models.CharField(max_length=50)
     tenencia_predio = models.CharField(max_length=50)
     modificacion_física_construccion = models.CharField(max_length=50)
     superficie_predio = models.CharField(max_length=50)
     municipio = models.CharField(max_length=50)
     ciudad_localidad = models.CharField(max_length=50)
     uso_predio = models.CharField(max_length=50)
     

class Datos_Construccion(models.Model):
     #fk_id_inmueble = models.ForeignKey(Datos_inmuebles, on_delete=models.CASCADE)
     fk_clave_catastral = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
     techos = models.CharField(max_length=20)
     pisos = models.CharField(max_length=20)
     muros = models.CharField(max_length=20)
     tipo_baños = models.CharField(max_length=20)
     instalacion_electrica = models.CharField(max_length=30)
     puertas_ventanas = models.CharField(max_length=20)
     edad = models.CharField(max_length=4)
     niveles = models.CharField(max_length=20)
     plano_croquis = models.CharField(max_length=2)
     doc_just_prop = models.CharField(max_length=2)
     ult_rec_imp = models.CharField(max_length=2)
     lic_obr_dem = models.CharField(max_length=2)


class Domicilio_inmueble(models.Model):
     
      #Inicializacion de los atributos del modelo Domicilio_inmueble

     pk_fk_clave_catastral = models.ForeignKey(Datos_Contribuyentes, on_delete=models.CASCADE)
     calle = models.CharField(max_length=35)
     col_fracc = models.CharField(max_length=35)
     num_int = models.CharField(max_length=5)
     num_ext = models.CharField(max_length=5)
     localidad = models.CharField(max_length=35)
     

#TABLAS/CLASES/MODELOS NUEVOS PARA LA BASE DE DATOS FICHA CATASTRAL

class datos_documento_predio(models.Model):

     pk_clave_catastral = models.CharField(primary_key=True,max_length=35)
     lugar_expedision = models.CharField(max_length=35)
     td = models.PositiveSmallIntegerField()
     num_documento = models.PositiveSmallIntegerField()
     dia = models.PositiveSmallIntegerField()
     mes = models.PositiveSmallIntegerField()
     año = models.PositiveSmallIntegerField()
     num_notaria = models.PositiveSmallIntegerField()


class datos_predio_ficha(models.Model):

     pk_clave_catastral = models.CharField(max_length=35)
     tipo_avaluo = models.PositiveSmallIntegerField()
     fraccionamiento = models.PositiveSmallIntegerField()
     traslado_dominio = models.PositiveSmallIntegerField()
     regimen = models.PositiveSmallIntegerField()
     tenencia = models.PositiveSmallIntegerField()
     estado_fisico = models.PositiveSmallIntegerField()
     codigo_uso = models.PositiveSmallIntegerField()
     tipo_posecion = models.PositiveSmallIntegerField()
     num_emision = models.PositiveSmallIntegerField()
     tipo_predio = models.PositiveSmallIntegerField()
     uso_predio = models.PositiveSmallIntegerField()


class datos_inscripcion(models.Model):

     pk_fk_clave_catastral = models.CharField(max_length=35)
     tipo = models.CharField(max_length=15)
     bajo_numero = models.PositiveSmallIntegerField()
     tomo = models.PositiveSmallIntegerField()
     dia_i = models.PositiveSmallIntegerField()
     mes_i = models.PositiveSmallIntegerField()
     año_i = models.PositiveSmallIntegerField()
     zona_i = models.PositiveSmallIntegerField()
     

class terrenos_rurales(models.Model):
     pk_fk_clave_catastral = models.CharField(max_length=35)
     tipo_suelo = models.PositiveSmallIntegerField()
     valor_has = models.PositiveSmallIntegerField()
     a = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     sup_has = models.PositiveSmallIntegerField()
     top = models.CharField(max_length=2)
     vias_c = models.CharField(max_length=2)


class terrenos_rurales_superficietotal(models.Model):
     pk_fk_clave_catastral = models.CharField(max_length=35)
     sup_t_has = models.PositiveSmallIntegerField()
     a = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     

class terrenos_urbanos_suburbanos(models.Model):
     fk_clave_catastral = models.CharField(max_length=35)
     valor_m2 = models.PositiveSmallIntegerField()
     area = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     frente = models.PositiveSmallIntegerField()
     profundidad = models.PositiveSmallIntegerField()
     valor = models.PositiveSmallIntegerField()


class demeritos_predios_urbanos(models.Model):
     fk_clave_catastral = models.CharField(max_length=35)
     descripcion =  models.CharField(max_length=35)
     valor  = models.PositiveSmallIntegerField()


class incrementos_esquina_urbanos(models.Model): 

     fk_clave_catastral = models.CharField(max_length=35)
     tipo =  models.CharField(max_length=1)
     valor  = models.PositiveSmallIntegerField()


class ficha_datos_construcciones(models.Model):
     etiqueta = models.CharField(max_length=1)
     fk_clave_catastral = models.ForeignKey(Datos_Contribuyentes,on_delete=models.CASCADE)
     tipo_c = models.PositiveSmallIntegerField()
     est =models.PositiveSmallIntegerField()
     terreno = models.PositiveSmallIntegerField()
     antiguedad = models.PositiveSmallIntegerField()
     area_c = models.PositiveSmallIntegerField() 

     class PK:
        # Especifica una restricción única para la combinación de modelo_a y otro_campo
        unique_together = ('etiqueta', 'fk_clave_catastral')

class valores_catastro(models.Model):
     clave_catastral_pk = models.CharField(max_length=35)
     valor_terreno = models.BigIntegerField()
     valor_construccion = models.BigIntegerField()
     valor_catastral = models.BigIntegerField()

class historial_pagos(models.Model):
     folio = models.CharField(max_length=6)
     contribuyente =  models.ForeignKey(Datos_Contribuyentes,on_delete=models.CASCADE)
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