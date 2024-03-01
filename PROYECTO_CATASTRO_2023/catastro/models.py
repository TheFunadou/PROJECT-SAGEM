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
    #fecha_registro= models.DateTimeField(auto_now_add=True)
    
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
     

# FICHA CATASTRAL///////////////////////////////////////////////////////////////////////////////////////

class fc_datos_generales(models.Model):
     folio = models.BigAutoField(primary_key=True)
     tipo_mov = models.CharField(max_length=2)
     fecha = models.DateTimeField(auto_now_add=True)
     clave_catastral= models.ForeignKey(Datos_Contribuyentes, on_delete= models.CASCADE)
     
class fc_datos_documento_predio(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     lugar_expedicion = models.CharField(max_length=35)
     td = models.PositiveSmallIntegerField()
     no_documento = models.PositiveSmallIntegerField()
     dia = models.PositiveSmallIntegerField()
     mes = models.PositiveSmallIntegerField()
     año = models.PositiveSmallIntegerField()
     no_notaria = models.PositiveSmallIntegerField()
     
class fc_datos_predio(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
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

class fc_datos_inscripcion(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     tipo = models.CharField(max_length=15)
     bajo_numero = models.PositiveSmallIntegerField()
     tomo = models.PositiveSmallIntegerField()
     dia = models.PositiveSmallIntegerField()
     mes = models.PositiveSmallIntegerField()
     year = models.PositiveSmallIntegerField()
     zona = models.PositiveSmallIntegerField()
     

class fc_datos_terrenos_rurales(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     tipo_suelo = models.PositiveSmallIntegerField()
     valor_has = models.PositiveSmallIntegerField()
     a = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     sup_has = models.PositiveSmallIntegerField()
     top = models.CharField(max_length=2)
     vias_c = models.CharField(max_length=2)

class fc_datos_terrenos_rurales_sup_total(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     sup_t_has = models.PositiveSmallIntegerField()
     a = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     

class fc_datos_terrenos_urbanos_suburbanos(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     valor_m2_1 = models.PositiveSmallIntegerField()
     area = models.PositiveSmallIntegerField()
     c = models.PositiveSmallIntegerField()
     valor_m2_2 = models.PositiveSmallIntegerField()
     frente = models.PositiveSmallIntegerField()
     profundidad = models.PositiveSmallIntegerField()
     
class fc_dtus_incremento_por_esquina(models.Model): 
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     tipo =  models.CharField(max_length=1)
     valor  = models.PositiveSmallIntegerField()


class fc_dtus_demeritos_predios_urbanos(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     descripcion =  models.CharField(max_length=35)
     valor  = models.PositiveSmallIntegerField()

class fc_datos_const(models.Model):
     folio_fc= models.ForeignKey(fc_datos_generales, on_delete=models.CASCADE)
     etiqueta = models.CharField(max_length=1)
     tipo_c = models.PositiveSmallIntegerField()
     estado = models.PositiveSmallIntegerField()
     terreno = models.PositiveSmallIntegerField()
     antiguedad = models.PositiveSmallIntegerField()
     area_d_m2 = models.IntegerField()
     class Meta:
         unique_together = ('folio_fc', 'etiqueta')

class fc_datos_construccion_valores(models.Model):
     folio_fc = models.ForeignKey(fc_datos_generales,on_delete= models.CASCADE)
     valor_terreno = models.BigIntegerField()
     valor_construccion = models.BigIntegerField()
     valor_catastral = models.BigIntegerField()

#CLASES PARA LOS PREDIOS Y CONTRIBUYENTES

class Datos_Gen_contribuyente(models.Model):

   rfc = models.CharField(primary_key=True,max_length=13)
   tipo_persona = models.CharField(max_length=30)
   tipo_identificacion = models.CharField(max_length=30)
   numero_identificacion = models.CharField(max_length=25)
   nombre = models.CharField(max_length=35)
   apaterno = models.CharField(max_length=35)
   amaterno = models.CharField(max_length=35)
   curp = models.CharField(max_length=18) 
   finado = models.CharField(max_length=2)
   fecha_nacimiento = models.CharField(max_length=10)
   telefono = models.CharField(max_length=10)
   telefono_movil = models.CharField(max_length=10)
   email = models.CharField(max_length=25)
   observaciones = models.CharField(max_length=100)



class Domicilio_noti(models.Model): 
    
   fk_rfc = models.ForeignKey(Datos_Gen_contribuyente, on_delete=models.CASCADE)
   entidad_fed = models.CharField(max_length=35)
   municipio = models.CharField(max_length=35)
   localidad = models.CharField(max_length=35)
   col = models.CharField(max_length=35)
   calle = models.CharField(max_length=35)
   cp = models.CharField(max_length=5)
   num_ext = models.CharField(max_length=5)
   letra_ext = models.CharField(max_length=5)
   num_int = models.CharField(max_length=5)
   letra_int = models.CharField(max_length=5)

class Datos_gen_predio(models.Model):

   clave_catastral = models.CharField(primary_key=True,max_length=30)
   cuenta_predial = models.CharField(max_length=30) 
   denominacion = models.CharField(max_length=25)  
   tipo_predio = models.CharField(max_length=30)
   uso_predio = models.CharField(max_length=20)
   region = models.CharField(max_length=30)
   zona_valor = models.CharField(max_length=30)
   cuenta_origen = models.CharField(max_length=30)
   fecha_alta = models.CharField(max_length=10)
   motivo_alta = models.CharField(max_length=30)
   #fecha_registro= models.DateTimeField(auto_now_add=True)


class Domicilio_predio(models.Model):

   fk_clave_catastral = models.ForeignKey(Datos_gen_predio, on_delete=models.CASCADE)
   entidad_fed = models.CharField(max_length=35)
   municipio = models.CharField(max_length=35)
   localidad = models.CharField(max_length=35)
   col = models.CharField(max_length=35)
   calle = models.CharField(max_length=35)
   #codigo_postal = models.CharField(max_length=10)
   num_ext = models.CharField(max_length=5)
   letra_ext = models.CharField(max_length=5)
   num_int = models.CharField(max_length=5)
   letra_int = models.CharField(max_length=5)
   ubic_coordenadas = models.CharField(max_length=35)


class predio_nuevo(models.Model):
    
   fk_clave_catastral = models.ForeignKey(Datos_gen_predio, on_delete=models.CASCADE)
   fk_rfc = models.ForeignKey(Datos_Gen_contribuyente, on_delete=models.CASCADE)
   porcentaje_part = models.CharField(max_length=5)


###########################################-------------

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