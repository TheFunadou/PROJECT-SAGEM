from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from django.utils import timezone
import json

from django.http import Http404, HttpResponseRedirect, HttpResponse,JsonResponse
# CREATE VIEW PARA GENERAR UNA CLASE PARA GUARDAR DATOS
from django.views.generic import CreateView
from notify.models import notify as notify_catastro
#TABLA USUARIOS
from django.contrib.auth.models import User, Group


#APLICACION CATASTRO
from catastro import models
from catastro.models import Datos_Contribuyentes,Domicilio_inmueble
from catastro.functions import send_notify
from .static.reports.DC017 import crear_reporte_DC017
from .static.reports.FICHA_CATASTRAL import crear_ficha_catastral
from .static.reports.REPORTE_TEST import REPORTE_TEST
from django.db import transaction, IntegrityError
#DJANGO NOTIFICACIONS

# channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#consultas filtradas
from django.db.models import Q

#transacciones
from django.db import transaction
from django.utils.timezone import localtime

current_app = 'CATASTRO'


#Funcion en testeo
def acceso_catastro(request):
    
    try:
        if request.user.is_authenticated:
            #Si es verdadero
            #Obtener el grupo al que pertenece el usuario
            grupo_user = request.user.groups.filter().first()
            if grupo_user:
                nom_grupo = grupo_user.name
                
            nom_grupo.lower()    
            nom_app = request.resolver_match.app_name
            
            if (nom_grupo != nom_app):
                if request.user.is_superuser:
                    return redirect(f'{nom_grupo}:perfil_su_{nom_grupo}')
                else:
                    return redirect(f'{nom_grupo}:perfil_{nom_grupo}')   
            
    except (Group.DoesNotExist):
        HttpResponse('El usuario no pertenece actualmente a ningun grupo')


def redirigir_user_cat(request):
    if request.user.is_authenticated:
            
            if request.user.is_superuser:
                if request.user.groups.filter()[0].name == 'CATASTRO':
                    return redirect('catastro:perfil_su_cat')
                if request.user.groups.filter()[0].name == 'FINANZAS':
                    return redirect('finanzas:perfil_su_fin')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
            else:
                if request.user.groups.filter()[0].name == 'CATASTRO':
                    return redirect('catastro:perfil_cat')
                elif request.user.groups.filter()[0].name == 'FINANZAS':
                    return redirect('finanzas:perfil_fin')
                elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                    return redirect('desarrollo_urbano:perfil_du')
    else:
        raise Http404("Usuario no autenticado")


# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')

@login_required(login_url="pag_login")
def redirigir_catastro(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect ("catastro:perfil_su_cat")
        else:
            return redirect("catastro:perfil_cat")
        
def obtener_username(request):
    nom_user = request.user.username
    
    obj_user = User.objects.get(username= nom_user)
    
    return obj_user

# Create your views here.
@login_required(login_url="pag_login")
def perfil_catastro(request):
    """
    
    """
    #REDIRECCIONAR A USUARIO QUE NO PERTENEZCAN A ESE DEPARTAMENTO
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su_catastro')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx={
        'url_pag': 'x',
        'nom_pag': 'Catastro',
        'titulo_pag': 'CATASTRO: CAJERO',
        'username':request.user.username
    }
    
    return render(request,'catastro/inicio_catastro.html',ctx)


# PERFIL SUPERUSUARIO

@login_required(login_url="pag_login")
def perfil_sup_user_catastro(request):
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
            ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_catastro')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx = {
        'notficaciones':'Notification.objects.values("description").filter()',
        'nom_pag': 'Catastro',
        'titulo_pag': 'CATASTRO: TITULAR',
        'username': request.user.username
    }

    return render(request, 'catastro/inicio_sup_user_catastro.html', ctx)


def view_prueba(request):
    return render (request,'catastro/prueba.html')

# Pantalla 
@login_required(login_url="pag_login")
def view_registrar_usuario(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
            ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
            
    
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'REGISTRO DE USUARIOS'
    }
    
    return render(request, 'catastro/registrar_usuario.html', ctx)

# RECIBIR DATOS DE LA VIEW REGISTRAR USUARIO
@login_required(login_url='pag_login')
def registrar_usuario(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    conf_password = request.POST['conf_password']
    departamento = request.POST['departamento']
    rol = request.POST['rol']
    
    
    if password == conf_password:
        # Crear nuevo usuario
        new_user= User(username=username, email=email)
        new_user.set_password(conf_password)
        
        if(rol == 'STAFF'):
            new_user.save()
        elif(rol == 'SUPER USUARIO'):
            new_user.is_superuser=True
            new_user.save()
            
        if departamento == 'INGRESOS':
            departamento = 'FINANZAS'
        
        # Asginar un grupo al usuario
        usuario = User.objects.get(username=username)
        grupo = Group.objects.get(name=departamento)
        
        usuario.groups.add(grupo)
        
        return redirigir_catastro(request)
    else:
        pass
    
    
# @login_required(login_url="pag_login")
# def views_cambiar_password(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             pass
#             ### DEMAS IF DE PERFILES DE SUPER USUARIO
#         else:
#             if request.user.groups.filter()[0].name == 'CATASTRO':
#                 return redirect('catastro:perfil_cat')
#             elif request.user.groups.filter()[0].name == 'FINANZAS':
#                 return redirect('finanzas:perfil_fin')
#             elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
#                 return redirect('desarrollo_urbano:perfil_du')
    
#     ctx = {
#         'nom_pag': 'Catastro',
#         'titulo_pag': 'RECUPERAR CONTRASEÑA'
#     }
    
#     return render(request, 'catastro/cambiar_password', ctx)

@login_required(login_url='pag_login')
def administrar_usuarios(request):
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su_catastro')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
            
    query_usuarios = User.objects.all()
    
    ctx ={
        "nom_pag": 'CATASTRO',
        'titulo_pag': 'BANDEJA DE NOTIFICACIONES',
        'nombre_user': request.user.username,
        # AQUI DEBO PASAR EL QUERY
    }
    
    
    return render(request, 'catastro/administrar_usuarios.html', ctx)


"""funciones para procesos de un contribuyente, alta, baja y modificacones"""
#vista pantalla consultas
@login_required(login_url="pag_login")
def vista_index_contribuyente(request):
    ctx = {
        'nom_pag': 'CATASTRO',
        'titulo_pag': 'BUSQUEDA DE CONTRIBUYENTES',
    }
    return render(request,'catastro/contribuyentes/index_contribuyente.html',ctx)

#consulta datos de los contribuyentes registrados
@login_required(login_url="pag_login")
def consulta_index_contribuyentes(request):
    consulta_general = []
    if request.method == 'POST':
        dato = request.POST['busqueda'].strip()
        if len(dato) == 0:
            consulta_general = models.Domicilio_noti.objects.all()
        else:
            consulta_general = models.Domicilio_noti.objects.filter(Q(fk_rfc__rfc = dato))

    return render(request,'catastro/contribuyentes/index_contribuyente.html', {'resultado': consulta_general,'titulo_pag': 'BUSQUEDA DE CONTRIBUYENTES' })

#vista registro ciudadano
@login_required(login_url="pag_login")
def vista_alta_contribuyente(request):
    return render(request,'catastro/contribuyentes/alta_contribuyentes.html', {'nom_pag': 'Catastro','titulo_pag': 'REGISTRO DE CIUDADANO',})

#REGISTRAR DATOS DEL CIUDADANO
@login_required(login_url="pag_login")
def registro_contribuyente(request):

    if request.method == 'POST':
        error_contribuyente = 0
        error_message =""
        rfc = request.POST['rfc']
        curp = request.POST['curp']

        if not (len(curp.strip()) == 0 or len(rfc.strip()) == 0):
            tipo_persona = request.POST['tipo_persona']
            tipo_identificacion = request.POST['tipo_identificacion']
            num_identificacion = request.POST['num_identificacion']
            nombre_razon = request.POST['nombre_razon']
            apaterno = request.POST['apaterno']
            amaterno = request.POST['amaterno']
            
            finado = request.POST['finado']
            fecha_nacimiento_registro = request.POST['fecha_nacimiento']
            telefono = request.POST['telefono']
            celular = request.POST['celular']
            email = request.POST['email']
            observaciones = request.POST['observaciones']
            error_contribuyente = 0

            if models.Datos_Gen_contribuyente.objects.filter(rfc=rfc).exists():
                error_message = f"Ya existe un registro con el RFC '{rfc}'"
                error_contribuyente = 1
            else:
                try:
                    models.Datos_Gen_contribuyente.objects.create(
                        rfc = rfc,
                        tipo_persona = tipo_persona,
                        tipo_identificacion = tipo_identificacion,
                        numero_identificacion = num_identificacion,
                        nombre = nombre_razon,
                        apaterno = apaterno,
                        amaterno = amaterno,
                        curp = curp,
                        finado = finado,
                        fecha_nacimiento = fecha_nacimiento_registro,
                        telefono = telefono,
                        telefono_movil = celular,
                        email = email,
                        observaciones = observaciones
                    )
                    error_contribuyente = 0
                    return registro_domicilio_contribuyente(request,rfc)
                except Exception as ex:
                    error_message = f"Error al registrar: {str(ex)}"
                    error_contribuyente = 1
        else:
            error_contribuyente = 1
            error_message = "RFC y CURP deben tener un valor"
            
            
    return render(request, 'catastro/contribuyentes/alta_contribuyentes.html', {'error_message': error_message, 'error_contribuyente':error_contribuyente})

#registra datos domicilio del contribuyente
@login_required(login_url="pag_login")
def registro_domicilio_contribuyente(request,fk_rfc):
   if request.method == 'POST':
        error_message =""
        error_domicilio = 0
        try:
            fk_rfc = fk_rfc
            entidad_fed = request.POST['entidad_federativa']
            municipio = request.POST['munic']
            localidad = request.POST['loca']
            col = request.POST['colon']
            calle = request.POST['calle']
            cp = request.POST['cp']
            num_ext = request.POST['num_ext']
            letra_ext = request.POST['let_ext']
            num_int = request.POST['num_int']
            letra_int = request.POST['let_int']
            
            models.Domicilio_noti.objects.create(
                fk_rfc = models.Datos_Gen_contribuyente.objects.get(rfc=fk_rfc), entidad_fed = entidad_fed,municipio = municipio,localidad = localidad,col = col,calle = calle,cp = cp,num_ext = num_ext,letra_ext = letra_ext,num_int = num_int,letra_int = letra_int
            )
            
        except Exception as e:
            error_message = f"Error al registrar: {str(e)}"
            error_domicilio = 1
   return render(request, 'catastro/contribuyentes/alta_contribuyentes.html', {'error_message': error_message, 'error_domicilio':error_domicilio})

#vista solo muestra pantalla de modificacion
@login_required(login_url="pag_login")
def vista_update_contribuyentes(request,rfc):
    
    consulta_a_modificar = models.Domicilio_noti.objects.filter(Q(fk_rfc__rfc = rfc))

    return render(request,'catastro/contribuyentes/modificacion_contribuyentes.html', {'nom_pag': 'Catastro','titulo_pag': 'MODIFICACION DE DATOS DEL CONTRIBUYENTE','consulta_contribuyente':consulta_a_modificar})

#funcion que actualiza los datos
@login_required(login_url="pag_login")
def update_contribuyentes(request,rfc_u):

    if request.method == 'POST':

        #rfc = request.POST['rfc']
        #tipo_persona = request.POST['tipo_persona']
        tipo_identificacion = request.POST['tipo_identificacion']
        num_identificacion = request.POST['num_identificacion']
        nombre_razon = request.POST['nombre_razon']
        apaterno = request.POST['apaterno']
        amaterno = request.POST['amaterno']
        #curp = request.POST['curp']
        finado = request.POST['finado']
        fecha_nacimiento_registro = request.POST['fecha_nacimiento']
        telefono = request.POST['telefono']
        celular = request.POST['celular']
        email = request.POST['email']
        observaciones = request.POST['observaciones']

        entidad_fed = request.POST['entidad_federativa']
        municipio = request.POST['munic']
        localidad = request.POST['loca']
        col = request.POST['colon']
        calle = request.POST['calle']
        cp = request.POST['cp']
        num_ext = request.POST['num_ext']
        letra_ext = request.POST['let_ext']
        num_int = request.POST['num_int']
        letra_int = request.POST['let_int']

        error_message =""

        if not len(rfc_u.strip()) == 0:

            try:

                with transaction.atomic():
                    consulta_mod =  models.Domicilio_noti.objects.filter(Q(fk_rfc__rfc = rfc_u))
                    for datos_mod in consulta_mod:
                        #datos principales contribuyente
                        datos_mod.fk_rfc.tipo_identificacion = tipo_identificacion
                        datos_mod.fk_rfc.numero_identificacion = num_identificacion
                        datos_mod.fk_rfc.nombre = nombre_razon
                        datos_mod.fk_rfc.apaterno = apaterno
                        datos_mod.fk_rfc.amaterno = amaterno
                        datos_mod.fk_rfc.finado = finado
                        datos_mod.fk_rfc.fecha_nacimiento = fecha_nacimiento_registro
                        datos_mod.fk_rfc.telefono = telefono
                        datos_mod.fk_rfc.telefono_movil = celular
                        datos_mod.fk_rfc.email = email
                        datos_mod.fk_rfc.observaciones = observaciones

                        #domicilio del contribuyente

                        datos_mod.entidad_fed =entidad_fed
                        datos_mod.municipio = municipio
                        datos_mod.localidad = localidad
                        datos_mod.col = col
                        datos_mod.calle = calle
                        datos_mod.cp = cp
                        datos_mod.num_ext = num_ext
                        datos_mod.letra_ext = letra_ext
                        datos_mod.num_int = num_int
                        datos_mod.letra_int = letra_int

                        datos_mod.fk_rfc.save()
                        datos_mod.save()

                        error_contribuyente = 0
            except Exception as e:
                error_message = f"Error de consulta: {str(e)}"
                error_contribuyente = 1

            ctx = {
                'error_message': error_message,
                'error_contribuyente':error_contribuyente
            }

    return render(request,'catastro/contribuyentes/modificacion_contribuyentes.html', ctx)

#función para eliminar un contribuyente
def delete_contribuyentes(request,rfc_u):

    if request.method == 'POST':
        error_message =""
        error_contribuyente_delete = 0
        if not len(rfc_u.strip()) == 0:
            try:
                consulta_delete = models.Datos_Gen_contribuyente.objects.filter(rfc=rfc_u)
                consulta_delete.delete()
                error_contribuyente_delete = 0
            except Exception as exc:
                error_message = f"Error de eliminación: {str(exc)}"
                error_contribuyente_delete = 1
                
    return render(request,'catastro/contribuyentes/index_contribuyente.html', {'error_message': error_message,'error_contribuyente':error_contribuyente_delete})

"""PROCESOS DE UN PREDIO. ALTA, BAJA, MODIDIFICACION Y CONSULTA"""   

#vista inicial de predios
def vista_index_predios(request):
    ctxp = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'BUSQUEDA DE PREDIOS',
    }
    return render(request,'catastro/predios/index_predios.html',ctxp)

#consulta de los predios registrados
def consulta_index_predios(request):
    if request.method == 'POST':
        dato = request.POST['busqueda'].strip()
        consulta_general = []

        if len(dato) == 0:
            consulta_general = models.Domicilio_predio.objects.all()
        else:
            consulta_general = models.Domicilio_predio.objects.filter(Q(fk_clave_catastral = dato))
        
    return render(request,'catastro/predios/index_predios.html', {'resultado_predios': consulta_general,'titulo_pag': 'BUSQUEDA DE PREDIOS'})

#vista de alta de predios
@login_required(login_url="pag_login")
def vista_alta_predios(request):
    ctxp = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'ALTA DE PREDIO',
    }
    return render(request,'catastro/predios/alta_predios.html', ctxp)


#registro de los predios nuevos
def registro_predios(request):
    if request.method== 'POST':

        error_mensaje_predio = ""
        error_predio = 0

        zona_cat = request.POST['zonacat']
        muni = request.POST['muni']
        loc = request.POST['loc']
        region = request.POST['region']
        manzana = request.POST['manzana']
        lote = request.POST['lote']
        nivel = request.POST['nivel']
        depto = request.POST['depto']
        dvs = request.POST['dvs']
 
        clave_catastral = zona_cat+muni+loc+region+manzana+lote+nivel+depto+dvs
        fecha_alta = request.POST['fecha_registro']
        motivo_alta = request.POST['motivo_registro']
        cuenta_predial =  request.POST['cuenta_predial']
        denominacion =  request.POST['denominacion']
        cuenta_origen = request.POST['cuenta_origen']
        tipo_predio = request.POST['tipo_predio']
        uso_predio = request.POST['uso_predio']
        region_2 = request.POST['region_2']
        zona_valor =request.POST['zona_valor']

        if models.Datos_gen_predio.objects.filter(clave_catastral=clave_catastral).exists():
                print('existe')
                error_mensaje_predio = f"Ya existe un registro con la clave catastral '{clave_catastral}'"
                error_predio = 1

        else: 

            try:


                    models.Datos_gen_predio.objects.create(
                        clave_catastral = clave_catastral,
                        cuenta_predial =  cuenta_predial,
                        denominacion =  denominacion ,
                        tipo_predio = tipo_predio,
                        uso_predio = uso_predio,
                        region = region_2,
                        zona_valor = zona_valor,
                        cuenta_origen = cuenta_origen,
                        fecha_alta = fecha_alta,
                        motivo_alta = motivo_alta,
                    )
                    error_predio = 0
                    return registro_domicilio_predios(request,clave_catastral)

            except Exception as ex:
                error_mensaje_predio = f"Error al registrar predio: {str(ex)}"
                error_predio = 1

    return render(request,'catastro/predios/alta_predios.html', {'error_mensaje_predio': error_mensaje_predio, 'error_predio':error_predio})
        
#registro de los domicilios de cada predio
def registro_domicilio_predios(request,clave):
    if request.method == 'POST':
        error_mensaje_predio = ""
        error_predio_domicilio = 0
       
        try:
            
            fk_clave_catastral = clave
            entidad_fed_p = request.POST['ent_federativa']
            municipio = request.POST['municipio_predio']
            localidad = request.POST['localidad_predio']
            col = request.POST['colonia_predio']
            calle = request.POST['calle_predio']
            num_ext = request.POST['num_exte_predio']
            letra_ext = request.POST['letra_exte_predio']
            num_int = request.POST['num_inte_predio']
            letra_int = request.POST['letra_inte_predio']
            ubic_coordenadas = 'XXXXX'


            models.Domicilio_predio.objects.create(

                fk_clave_catastral = models.Datos_gen_predio.objects.get(clave_catastral=fk_clave_catastral),
                entidad_fed = entidad_fed_p,
                municipio = municipio,
                localidad = localidad,
                col = col,
                calle = calle,
                num_ext = num_ext,
                letra_ext = letra_ext,
                num_int = num_int,
                letra_int = letra_int,
                ubic_coordenadas = ubic_coordenadas

            )
            
        
        except Exception as e:
            error_mensaje_predio = f"Error al registrar domicilio: {str(e)}"
            error_predio_domicilio = 1
    return render(request, 'catastro/predios/alta_predios.html', {'error_mensaje_predio': error_mensaje_predio, 'error_predio_domicilio':error_predio_domicilio})

#vista para actualizar la información de cada predio
def vista_update_predios(request, clave_cat):

    consulta_a_modificar_predios = models.Domicilio_predio.objects.filter(Q(fk_clave_catastral__clave_catastral = clave_cat))

    con = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'MODIFICACION DE DATOS DEL PREDIO',
        'consulta_predios':consulta_a_modificar_predios
    }

    return render(request,'catastro/predios/modificacion_predios.html', con)

#función que actualiza la información 
def update_predios(request, clave_cat):
     
    if request.method == 'POST':

        fecha_alta = request.POST['fecha_registro']
        motivo_alta = request.POST['motivo_registro']
        cuenta_predial =  request.POST['cuenta_predial']
        denominacion =  request.POST['denominacion']
        cuenta_origen = request.POST['cuenta_origen']
        tipo_predio = request.POST['tipo_predio']
        uso_predio = request.POST['uso_predio']
        region_2 = request.POST['region_2']
        zona_valor =request.POST['zona_valor']

        entidad_fed = request.POST['ent_federativa']
        municipio = request.POST['municipio_predio']
        localidad = request.POST['localidad_predio']
        col = request.POST['colonia_predio']
        calle = request.POST['calle_predio']
        num_ext = request.POST['num_exte_predio']
        letra_ext = request.POST['letra_exte_predio']
        num_int = request.POST['num_inte_predio']
        letra_int = request.POST['letra_inte_predio']

        error_mensaje_predio =""

        if not len(clave_cat.strip()) == 0:

            try:

                with transaction.atomic():

                    consulta_mod =  models.Domicilio_predio.objects.filter(Q(fk_clave_catastral__clave_catastral = clave_cat))

                    for datos_mod in consulta_mod:

                        #datos principales predio
                        datos_mod.fk_clave_catastral.cuenta_predial = cuenta_predial
                        datos_mod.fk_clave_catastral.denominacion = denominacion
                        datos_mod.fk_clave_catastral.tipo_predio = tipo_predio
                        datos_mod.fk_clave_catastral.uso_predio = uso_predio
                        datos_mod.fk_clave_catastral.region = region_2
                        datos_mod.fk_clave_catastral.zona_valor = zona_valor
                        datos_mod.fk_clave_catastral.cuenta_origen = cuenta_origen
                        datos_mod.fk_clave_catastral.fecha_alta = fecha_alta
                        datos_mod.fk_clave_catastral.motivo_alta = motivo_alta


                        #domicilio del contribuyente

                        datos_mod.entidad_fed =entidad_fed
                        datos_mod.municipio = municipio
                        datos_mod.localidad = localidad
                        datos_mod.col = col
                        datos_mod.calle = calle
                        datos_mod.num_ext = num_ext
                        datos_mod.letra_ext = letra_ext
                        datos_mod.num_int = num_int
                        datos_mod.letra_int = letra_int

                        datos_mod.fk_clave_catastral.save()
                        datos_mod.save()

                        error_predio = 0


            except Exception as e:
                error_mensaje_predio = f"Error de consulta: {str(e)}"
                error_predio = 1

            ctx = {
                'error_message': error_mensaje_predio,
                'error_predio':error_predio
            }

    return render(request,'catastro/predios/modificacion_predios.html', ctx)

#función para eliminar un predio
def delete_predios(request, clave_cat):
    if request.method == 'POST':

        error_mensaje_predio =""
        error_predio_delete = 0

    
        if not len(clave_cat.strip()) == 0:
           

            try:
   
                consulta_predio_delete = models.Datos_gen_predio.objects.filter(clave_catastral=clave_cat)
                consulta_predio_delete.delete()
                error_predio_delete = 0
            
            except Exception as exc:

                error_mensaje_predio = f"Error de eliminación: {str(exc)}"
                error_predio_delete = 1



    return render(request,'catastro/predios/index_predios.html', {
                'error_mensaje_predio': error_mensaje_predio,
                'error_predio':error_predio_delete
            })

"""-----------------------------------------"""


"""PROCESOS ASIGNACIÓN DE PROPIETARIOS A UN PREDIO"""

#vista inicial
def vista_index_asignacion(request):
    context_a = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO',
    }
    return render(request,'catastro/asignacion_propietario/index_asignacion.html',context_a)

#vista para registro
def vista_alta_asignacion(request):
    context_a = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'ASIGNACIÓN NUEVA',
    }
    return render(request,'catastro/asignacion_propietario/alta_asignacion.html', context_a)


"""-----------------------------------------"""





"""PROCESO SOLICITU DC017"""

#Buscar si la clave catastral del predio está previamente registrada

def buscar_predio_dc017(request, *args,**kwargsst):

    lista = []
    clave = request.GET.get('search')

    if clave:

        print(clave)

        

        #predio = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral__startswith = search) | Q(pk_fk_clave_catastral__nombre__startswith = search) 
                                                    #| Q(pk_fk_clave_catastral__apaterno__startswith = search) | Q(pk_fk_clave_catastral__amaterno__startswith = search)) 

        predio = models.Domicilio_predio.objects.select_related().filter(Q(fk_clave_catastral__clave_catastral__startswith = clave)) 
        print(predio)

        for dato in predio:

            lista.append({
                #datos generales del predio
                'clave_catastral': dato.fk_clave_catastral.clave_catastral,
                'tipo_predio': dato.fk_clave_catastral.tipo_predio,
                'uso_predio': dato.fk_clave_catastral.uso_predio,

                #domicilio del predio
                'calle':dato.calle,
                'num_int':dato.num_int,
                'num_ext':dato.num_ext,
                'col':dato.col,
                'localidad':dato.localidad,
                'municipio' : dato.municipio
                
            })
   

    return JsonResponse({
                    'status': True,
                    'payload':lista
                })

    

def buscar_contribuyente_dc017(request, *args,**kwargsst):
    lista = []
    rfc = request.GET.get('search')

    if rfc:

        print(rfc)

        

        #predio = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral__startswith = search) | Q(pk_fk_clave_catastral__nombre__startswith = search) 
                                                    #| Q(pk_fk_clave_catastral__apaterno__startswith = search) | Q(pk_fk_clave_catastral__amaterno__startswith = search)) 

        contribuyente = models.Domicilio_noti.objects.filter(Q(fk_rfc__rfc__startswith = rfc))   
        
        print(contribuyente)

        for dato in contribuyente:

            lista.append({
                #datos generales del contribuyente
                'rfc': dato.fk_rfc.rfc,
                'nombre': dato.fk_rfc.nombre,
                'apaterno': dato.fk_rfc.apaterno,
                'amaterno': dato.fk_rfc.amaterno,

                #domicilio del contribuyente
                'telefono_movil': dato.fk_rfc.telefono_movil,
                'calle':dato.calle,
                'num_int':dato.num_int,
                'num_ext':dato.num_ext,
                'cp':dato.num_ext,
                'col':dato.col,
                'localidad':dato.localidad,
                
            })
   

    return JsonResponse({
                    'status': True,
                    'payload':lista
                })


@login_required(login_url="pag_login")
#vista solicitud dc017
def solicitud_dc017(request):
    return render(request,'catastro/solicitud_dc017.html', {'nom_pag': 'Catastro','titulo_pag': 'SOLICITUD DC017',})

def registrar_solicitud_dc017(request):
    clave_cat = request.POST['busqueda']
    print(F'LA CLAVE CATASTRAL ES : {clave_cat}')
    apaterno = request.POST['apaterno']
    amaterno = request.POST['amaterno']
    nombre = request.POST['nombre']
    rfc = request.POST['rfc']
    telefono = request.POST['telefono']
    tipo = request.POST.get('tipo_tel')
    calle = request.POST['calle']
    colonia_fraccionamiento = request.POST['colonia_fraccionamiento']
    num_int = request.POST['num_int']
    num_ext = request.POST['num_ext']
    localidad = request.POST['localidad']
    codigo_postal = request.POST['codigo_postal']

    #Almacenar info gral del DC017 
    models.Datos_Contribuyentes.objects.create(
        clave_catastral=clave_cat,
        rfc=rfc,
        nombre=nombre,
        apaterno=apaterno,
        amaterno=amaterno,
        telefono=telefono,
        tipo=tipo,
        calle=calle,
        num_int=num_int,
        num_ext=num_ext,
        colonia_fraccionamiento=colonia_fraccionamiento,
        localidad=localidad,
        codigo_postal=codigo_postal)
    
    calle = request.POST['calle2']
    col_fracc = request.POST['col_fracc']
    num_int = request.POST['ni']
    num_ext=request.POST['ne']
    localidad = request.POST['localidad']

    # Enlazar info del domicilio con la clave_cat del contribuyente
    models.Domicilio_inmueble.objects.create(
        pk_fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat),
        calle=calle,
        num_int=num_int,
        num_ext=num_ext,
        col_fracc=col_fracc,
        localidad=localidad
    )

    #DATOS DEL INMUEBLE
    estado_fisico = request.POST['estadofisico']
    tipo_predios = request.POST['tipopredio']
    tenencia_predios = request.POST['tenenciapredio']
    modificacion_fisica = request.POST['modificacion']
    superficie = request.POST['superficie']
    municipio = request.POST['municipio2']
    ciudad = request.POST['ciudad2']
    uso_destino = request.POST['uso']

    #DATOS DE LA CONSTRUCCION
    techos = request.POST['techos']
    pisos = request.POST['pisos']
    muros = request.POST['muros']
    tipo_baños = request.POST['tipobaño']
    instalacion_electrica = request.POST['instalacionelectrica']
    puertas_ventanas = request.POST['puertaventana']
    edad_años = request.POST['años']
    niveles = request.POST['niveles']
    plan_croq= 'SI' if 'P_O_C' in request.POST else 'NO'
    doc_just= 'SI' if 'DOC_JUST' in request.POST else 'NO'
    ult_rec= 'SI' if 'U_R_I' in request.POST else 'NO'
    lic_obr= 'SI' if 'LIC_OB' in request.POST else 'NO'
    

    models.Datos_inmuebles.objects.create(
        pk_estado_fisico_predio=estado_fisico,
        tipo_predio=tipo_predios,
        tenencia_predio=tenencia_predios,
        modificacion_física_construccion=modificacion_fisica,
        superficie_predio=superficie,
        municipio=municipio,
        ciudad_localidad=ciudad,
        uso_predio=uso_destino,
        fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    )
    
    models.Datos_Construccion.objects.create(
        fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat),
        techos=techos,
        pisos=pisos,
        muros=muros,
        tipo_baños=tipo_baños,
        instalacion_electrica=instalacion_electrica,
        puertas_ventanas=puertas_ventanas,
        edad=edad_años,
        niveles=niveles,
        plano_croquis = plan_croq,
        doc_just_prop = doc_just,
        ult_rec_imp = ult_rec,
        lic_obr_dem = lic_obr
    )
    crear_reporte_DC017(clave_cat,request.user.username)
    return redirect('catastro:redirigir_perfil_cat')
    

"""---FICHA CATASTRAL"""
"""--- APARTADO 1 DATOS GENERALES ---"""
#CONSULTAR DATOS GENERALES DEL CONTRIBUYENTES PARA FICHA CATASTRAL
def obtener_datos_busqueda_ficha(request, *args,**kwargs):
    search = request.GET.get('search')
    lista = []

    if search:
        con = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral__startswith = search) | Q(pk_fk_clave_catastral__nombre__startswith = search) 
                                                        | Q(pk_fk_clave_catastral__apaterno__startswith = search) | Q(pk_fk_clave_catastral__amaterno__startswith = search)) 
        for dato in con:
            lista.append({
                #datos generales
                'clave_catastral': dato.pk_fk_clave_catastral.clave_catastral,
                'nombre': dato.pk_fk_clave_catastral.nombre,
                'apaterno': dato.pk_fk_clave_catastral.apaterno,
                'amaterno': dato.pk_fk_clave_catastral.amaterno,
                'rfc':dato.pk_fk_clave_catastral.rfc,
                #domicilio del contribuyente
                'calle_con':dato.pk_fk_clave_catastral.calle,
                'int_con':dato.pk_fk_clave_catastral.num_int,
                'ext_con':dato.pk_fk_clave_catastral.num_ext,
                'codigo_postal':dato.pk_fk_clave_catastral.codigo_postal,
                'colonia_fraccionamiento_con':dato.pk_fk_clave_catastral.colonia_fraccionamiento,
                'localidad_con':dato.pk_fk_clave_catastral.localidad,
                #domicilio del predio
                'calle':dato.calle,
                'colonia':dato.col_fracc,
                'localidad':dato.localidad,
                'num_ext':dato.num_ext,
                'num_int':dato.num_int,
            })

        # print(lista)

    return JsonResponse({
        'status': True,
        'payload':lista
    })

def consultar_datos_generales(request,clave,*args,**kwargs):

        lista_contribuyentes = []
        
        data = models.Datos_Contribuyentes.objects.filter(clave_catastral=clave)   
        # print(data)
        for contribuyente in data:
            contribuyentes_datos = {}
            contribuyentes_datos['clave_catastral'] = contribuyente.clave_catastral
            contribuyentes_datos['rfc'] = contribuyente.rfc
            contribuyentes_datos['nombre'] = contribuyente.nombre
            contribuyentes_datos['apaterno'] = contribuyente.apaterno
            contribuyentes_datos['amaterno'] = contribuyente.amaterno
            contribuyentes_datos['calle'] = contribuyente.calle
            contribuyentes_datos['num_int'] = contribuyente.num_int
            contribuyentes_datos['num_ext'] = contribuyente.num_ext
            contribuyentes_datos['colonia_fraccionamiento'] = contribuyente.colonia_fraccionamiento
            contribuyentes_datos['localidad'] = contribuyente.localidad
            contribuyentes_datos['codigo_postal'] = contribuyente.codigo_postal
            lista_contribuyentes.append(contribuyentes_datos)
        # print(lista_contribuyentes)
        data = json.dumps(lista_contribuyentes)
        return HttpResponse(data,'application/json')
   
@login_required(login_url="pag_login")
#vista ficha catastral
def ficha_catastral(request):
    return render(request,'catastro/ficha_catastral.html', {'fecha_hoy':localtime().date(), 'nom_pag':'Catastro','titulo_pag': 'FICHA CATASTRAL'})

def view_ficha_catastral(request):
    try:
        
        if request.method == 'GET':
            clave_cat = request.GET.get('clave_cat')
            tipo_mov = request.GET.get('tipo_mov')
            list_DDPP = request.GET.getlist('dtos_doc_pred[]')
            list_DP = request.GET.getlist('dtos_pred[]')
            list_IRPP_ACT = request.GET.getlist('dtos_irpp_act[]')
            list_IRPP_ANT = request.GET.getlist('dtos_irpp_ant[]')
            list_table_tr = request.GET.get('dtos_tr')
            list_TR_TOP_VIAS = request.GET.getlist('dtos_tr_top_vias[]')
            list_TR_SUP_T = request.GET.getlist('dtos_tr_st[]')
            list_DTUS = request.GET.get('dtos_dtus')
            list_DTUS_IXE = request.GET.getlist('dtos_dtus_ixe[]')
            list_DTUS_DPU = request.GET.getlist('dtos_dtus_dpu[]')
            list_DC = request.GET.get('dtos_const')
            list_DC_V = request.GET.getlist('dtos_const_v[]')
        
        """ print(f'Clave catastral: {clave_cat}')
        print(f'Tipo Mov: {tipo_mov}')
        print('datos documento de propiedad o posesion')
        print(list_DDPP)
        print('datos del predio')
        print(list_DP)
        print('datos de inscripcion en el regsitro publico de la propiedad actual')
        print(list_IRPP_ACT)
        print('datos de inscripcion en el regsitro publico de la propiedad antecedente')
        print(list_IRPP_ANT)
        print('datos terrenos rurales')
        print(list_table_tr)
        # Tabla Datos Terrenos Rurales
        table_tr = json.loads(list_table_tr)
        
        for array in table_tr:
            for item in array:
                print(item)
        print('datos terrenos rurales superficie total TOP VIAS:')
        print(list_TR_TOP_VIAS)
        print('datos terrenos rurales superficie total:')
        print(list_TR_SUP_T)
        print('datos terrenos urbanos y suburnano:')
        # Tabla Datos Terrenos Urbanos y Suburbanos
        table_dtus = json.loads(list_DTUS)
        for array in table_dtus:
            for item in array:
                print(item)
        print('datos terrenos urbanos y suburnanos incremento por esquina:')
        print(list_DTUS_IXE)
        print('datos terrenos urbanos y suburnanos demeritos:')
        print(list_DTUS_DPU)
        print('datos construccion:')
         # Tabla Datos Construccion
        table_dc = json.loads(list_DC)
        
        for array in table_dc:
            for item in array:
                print(item)
        print(list_DC_V)"""
        
        contribuyente = models.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
        print(list_table_tr)
        
        #Transaccion para el guardado de datos de la ficha catastral
        with transaction.atomic():
            # Guardar datos generales de la ficha
            ficha_cat = models.fc_datos_generales.objects.create(
                tipo_mov = tipo_mov,fecha = timezone.now(), clave_catastral= contribuyente
            )
            
            #Obtener el folio perteneciente a esta ficha catastral con nuestra variable ficha_cat.folio
            folio_ficha_cat = models.fc_datos_generales.objects.get(folio = ficha_cat.folio)
            
            #Guardar datos documento predio
            models.fc_datos_documento_predio.objects.create(
                folio_fc= folio_ficha_cat, lugar_expedicion= list_DDPP[0], td = list_DDPP[1],
                no_documento = list_DDPP[2], dia = list_DDPP[3], mes = list_DDPP[4], año= list_DDPP[5],
                no_notaria = list_DDPP[6]
            )
            
            #Guardar datos del predio
            models.fc_datos_predio.objects.create(
                folio_fc= folio_ficha_cat,tipo_avaluo = list_DP[0], fraccionamiento = list_DP[1], traslado_dominio = list_DP[2],
                regimen = list_DP[3], tenencia = list_DP[4], estado_fisico = list_DP[5], codigo_uso = list_DP[6], tipo_posecion = list_DP[7],
                num_emision = list_DP[8], tipo_predio = list_DP[9], uso_predio = list_DP[10]
            )
            
            #Guardar datos de inscripcion ACTUAL
            models.fc_datos_inscripcion.objects.create(
                folio_fc= folio_ficha_cat,tipo = 'ACTUAL', bajo_numero = list_IRPP_ACT[0], tomo = list_IRPP_ACT[1],
                dia = list_IRPP_ACT[2], mes = list_IRPP_ACT[3], year = list_IRPP_ACT[4], zona = list_IRPP_ACT[5]
            )
            
            #Guardar datos inscripcion ANTECEDENTE
            models.fc_datos_inscripcion.objects.create(
                folio_fc= folio_ficha_cat,tipo = 'ANTECEDENTE', bajo_numero = list_IRPP_ANT[0], tomo = list_IRPP_ANT[1],
                dia = list_IRPP_ANT[2], mes = list_IRPP_ANT[3], year = list_IRPP_ANT[4], zona = list_IRPP_ANT[5]
            )

            #Cargar lista serializada list_table_tr(Datos de terrenos rurales) con json.loads
            tabla_terrenos_rurales = json.loads(list_table_tr)
            # Tabla Datos Terrenos Rurales
            
            #Validacion para comprobar si la tabla esta vacia, si es verdadero no se hace nada, si es falso
            #Se guarda la informacion de datos de terrenos rurales
            if not tabla_terrenos_rurales:
                # print('TABLA TERRENOS RURALES ESTA VACIA')
                pass
            else:
                # print('TABLA TERRENOS RUARALES CONTIENE INFORMACION')
                #Recorrer lista de tabla_terrenos_rurales la cual contiene sublistas: ejemplo [[x,y,z],[x,y,z]]
                for array in tabla_terrenos_rurales:
                    #Guardar informacion en datos_terrenos_rurales accediendo a los indices de cada sublista
                    models.fc_datos_terrenos_rurales.objects.create(
                        folio_fc=folio_ficha_cat, tipo_suelo=array[0],
                        valor_has=array[1],sup_has=array[2],
                        a=array[3],c=array[4],top=list_TR_TOP_VIAS[0], 
                        vias_c=list_TR_TOP_VIAS[1] 
                    )
                
                #Guardar infromacion de superfice total de los datos de terrenos rurales
                models.fc_datos_terrenos_rurales_sup_total.objects.create(
                folio_fc = folio_ficha_cat, sup_t_has = list_TR_SUP_T[0],
                a = list_TR_SUP_T[1],c = list_TR_SUP_T[2]
                )
            
            
            # Tabla Datos Terrenos Urbanos y Suburbanos
            #Cargar lista serializada de datos de terrenos urbanos y suburbanos
            #Validacion para comprobar si la tabla esta vacia, si es verdadero no se hace nada, si es falso
            #Se guarda la informacion de datos de terrenos rurales
            table_datos_tus = json.loads(list_DTUS)
            if not table_datos_tus:
                pass
            else:
                #Recorrer lista de tabla_terrenos_rurales la cual contiene sublistas: ejemplo [[x,y,z],[x,y,z]]
                for array in table_datos_tus:
                    #Guardar informacion en terrenos urbanos y suburbanos accediendo a los indices de cada sublista
                    models.fc_datos_terrenos_urbanos_suburbanos.objects.create(
                        folio_fc=folio_ficha_cat, valor_m2_1=array[0],
                        area=array[1], c=array[2], valor_m2_2=array[3],
                        frente=array[4], profundidad=array[5], 
                    )
                
                #Lista donde se almacenan los "tipos" de la tabla datos terrenos urbanos y suburbanos de los incrementos por esquina
                list_tipo_dtus = ['A','B','C','D'] 
                #Ciclo for de los listas usando zip para recorrer ambas listas al mismo tiempo
                for item, item_2 in zip(list_tipo_dtus, list_DTUS_IXE):
                    models.fc_dtus_incremento_por_esquina.objects.create(
                        folio_fc =folio_ficha_cat, tipo = item, valor = item_2
                    )
                
                #Lista donde se almacenan la "descripcion" de la tabla datos terrenos urbanos y suburbanos de los demeritos predio urbanos
                list_descripcion_dtus_dpu = ['INTERES SOCIAL','EXCEDENTE DE AREA', 'TOPOGRAFIA', 'COND. FISICA IMPREVISTA']
                #Ciclo for de los listas usando zip para recorrer ambas listas al mismo tiempo
                for item, item_2 in zip(list_descripcion_dtus_dpu, list_DTUS_DPU):
                    models.fc_dtus_demeritos_predios_urbanos.objects.create(
                        folio_fc =folio_ficha_cat, descripcion = item, valor = item_2
                    )
            
            # Tabla Datos Construccion
            table_datos_const = json.loads(list_DC)
            if not list_DC:
                pass
            else:
                for array in table_datos_const:
                    models.fc_datos_const.objects.create(
                        folio_fc=folio_ficha_cat, etiqueta=array[0], tipo_c=array[1],
                        estado=array[2], terreno=array[3], antiguedad=array[4],
                        area_d_m2=array[5],
                    )
            
            # Tabla Datos Construccion Valores
            models.fc_datos_construccion_valores.objects.create(
                folio_fc = folio_ficha_cat, valor_terreno = list_DC_V[0],
                valor_construccion = list_DC_V[1], valor_catastral = list_DC_V[2]
            )
            
    except IntegrityError:
       return JsonResponse()
    transaction.commit()
    return JsonResponse({'MENSAJE':'DATOS GUARDADOS EXITOSAMENTE.'})

@login_required(login_url='pag_login')
def cambiar_password(request):
    username = request.POST['username']
    password = request.POST['password']
    conf_password = request.POST['conf_password']

def view_notify(request):
    return render(request,'catastro/notification_2.html')

def gen_reporte_dc017(request):
    clave_cat = request.POST['clave_cat']
    
    # crear_reporte_DC017(clave_cat)
    REPORTE_TEST()
        
    return HttpResponse('ok')
    
def send_notify_test(request):

    acceso_catastro(request)
    
    remitente = request.user.username
    destinatario = request.POST['destinatario']
    id_dest = User.objects.get(username=destinatario)
    titulo = request.POST['titulo']
    cuerpo = request.POST['cuerpo']

    """
     notify_catastro.objects.create(
        remitente=remitente,
        destinatario = id_dest,
        titulo = titulo,
        cuerpo = cuerpo
    )
    
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'consumer_notifications_{destinatario}',
        {
            'type':'update_not',
            'destinatario': destinatario
        }
    )
    
    """

    send_notify(remitente,destinatario,titulo, cuerpo)    
    
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'consumer_notifications',
    #     {
    #         'type':'update_not',
    #         'destinatario': destinatario
    #     }
    # )
    
    
    return HttpResponse('Notificacion enviada')

def gestor_notify_catastro(request):
    
    notify_d = notify_catastro.objects.all().filter(destinatario = obtener_username(request))
    
    
    ctx ={
        "nom_pag": 'CATASTRO',
        'titulo_pag': 'BANDEJA DE NOTIFICACIONES',
        'nombre_user': request.user.username,
        'notify':notify_d
    }
    
    return render(request,'catastro/gestor_notify_catastro.html',ctx)
    
    
def migrar_contribuyentes(request):
    return render (request,'catastro/migrar_contrib.html',{"nom_pag":'CATASTRO','titulo_pag': 'MIGRAR CONTRIBUYENTES',})
