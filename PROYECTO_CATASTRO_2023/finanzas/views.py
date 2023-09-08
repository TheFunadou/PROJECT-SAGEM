from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from notify.models import notify as notify_finanzas
from django.contrib.auth.models import User

from catastro import models as models_catastro
from finanzas import models as models_finanzas
from catastro.models import Domicilio_inmueble

import datetime
import json
import random
import re
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlencode
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse

from django.views.decorators.csrf import requires_csrf_token
from django.db.models import Q

# CHANNEL LAYERS
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .reports.reporte_pago_predial_ad import reporte_pago_predial_ad
from .reports.reporte_pago_predial_c import reporte_pago_predial_corriente


#Mandar una notificacion
def send_notify(remitente, destinatario, titulo, cuerpo):
    
    id_dest = User.objects.get(username=destinatario)
    
    notify_finanzas.objects.create(
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

# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')

#Obtener username como objecto tipo user
def obtener_username(request):
    nom_user = request.user.username
    
    obj_user = User.objects.get(username= nom_user)
    
    return obj_user
    
@login_required(login_url="pag_login")
def redirigir_finanzas(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect ("finanzas:perfil_su_fin")
        else:
            return redirect("finanzas:perfil_fin")

# Create your views here.
@login_required(login_url="pag_login")
def perfil_finanzas(request):
    
    #REDIRECCIONAR A USUARIO QUE NO PERTENEZCAN A ESE DEPARTAMENTO
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
                # SU DESARROLLO URBANO
                # SU FINANZAS
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                    return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx={
        'nom_pag': 'INGRESOS',
        'titulo_pag': 'INICIO INGRESOS',
        'nombre_user': request.user.username
    }
    
    return render(request,'finanzas/inicio_finanzas.html',ctx)


# PERFIL SUPERUSUARIO

@login_required(login_url="pag_login")
def perfil_sup_user_finanzas(request):
    
    #CODIGO PARA REVISAR Y REDIRECCIONAR DEPENDIENDO DEL GRUPO AL QUE PERTENECE AL USUARIO
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su_cat')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
                # SU DESARROLLO URBANO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    #CONTEXTO PARA EL TEMPLATE
    ctx = {
        'nom_pag': 'INGRESOS',
        'titulo_pag': 'INICIO SUPER USUARIO INGRESOS',
        'nombre_user': request.user.username
    }

    return render(request, 'finanzas/inicio_sup_user_finanzas.html', ctx)


@login_required(login_url="pag_login")
def gestor_notify_finanzas(request):

    
    notify_d = notify_finanzas.objects.all().filter(destinatario = obtener_username(request))
    
    ctx ={
        "nom_pag": 'INGRESOS',
        'titulo_pag': 'BANDEJA DE NOTIFICACIONES',
        'nombre_user': request.user.username,
        'notify':notify_d
    }
    
    return render (request,'finanzas/gestor_notify_finanzas.html',ctx)


"""------------------------------FINANZAS---------------------------------------"""
#APARTADO DE FINANZAS PAGO PREDIAL 


## --- EL CONTRIBUYENTE VA AL CORRIENTE

#PANTALLA PARA BUSQUEDA DEL CONTRIBUYENTE 
def buscar_adeudos(request):
    ctx={
        'titulo_pag': 'PAGO PREDIAL: BUSQUEDA DE CONTRIBUYENTE',
    }
    return render(request, "finanzas/pago-predial/busqueda_contribuyente_1.html",ctx)

#FUNCIÓN (AJAX) QUE HACE BUSQUEDA DE TODOS LOS DATOS DEL CONTRIBUYENTE EN  TIEMPO REAL
def obtener_datos_busqueda(request, *args,**kwargs):
    search = request.GET.get('search')
    lista = []

    if search:

        con = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral__startswith = search) | Q(pk_fk_clave_catastral__nombre__startswith = search) 
                                                        | Q(pk_fk_clave_catastral__apaterno__startswith = search) | Q(pk_fk_clave_catastral__amaterno__startswith = search)) 
         

        for dato in con:
            lista.append({
                'clave_catastral': dato.pk_fk_clave_catastral.clave_catastral,
                'nombre': dato.pk_fk_clave_catastral.nombre,
                'apaterno': dato.pk_fk_clave_catastral.apaterno,
                'amaterno': dato.pk_fk_clave_catastral.amaterno,
                'calle':dato.calle,
                'colonia':dato.col_fracc,
                'localidad':dato.localidad,
                'num_ext':dato.num_ext,
                
            })

    return JsonResponse({
        'status': True,
        'payload':lista
    })

#CONSULTA DE DATOS DEL CONTRIBUYENTE PARA MOSTRAR EN LA PANTALLA DE PAGO DE PREDIO
def pago_predial_datos_1(request,dato):
    lista = []
    est_fisico_predio = ''
    tipo_predio = ''
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 

    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio


    for data in extraer_datos_contribuyente:
       lista.append({
           'clave_catastral':data.pk_fk_clave_catastral.clave_catastral,
           'apellido_paterno':data.pk_fk_clave_catastral.apaterno,
           'apellido_materno':data.pk_fk_clave_catastral.amaterno,
           'nombre':data.pk_fk_clave_catastral.nombre,
           'calle_s':data.calle,
           'num_int':data.num_int,
           'num_ext':data.num_ext,
           'colonia_f':data.col_fracc,
           'estado_fisico':est_fisico_predio,
           'tipo_predio':tipo_predio
       })

    context = {
        'nom_pag': 'INGRESOS',
        'titulo_pag': 'ADEUDOS DEL CONTRIBUYENTE',
        'my_list': lista
        
    }

    

    return render(request,"finanzas/pago-predial/datos_consultados_contribuyente_1.html",context)




# --- CONTRIBUYENTE DEBE AÑOS
#PANTALLA PARA BUSQUEDA DEL CONTRIBUYENTE 
def pago_predial_busqueda_2(request):
    return render(request, "finanzas/pago-predial/busqueda_contribuyente_2.html")

#CONSULTA DE DATOS DEL CONTRIBUYENTE PARA MOSTRAR EN LA PANTALLA DE PAGO DE PREDIO
def pago_predial_datos_2(request,dato):
    lista = []
    lista_adeudos =[]
    est_fisico_predio = ''
    tipo_predio = ''
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato))

    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    pagos_adeudo = models_finanzas.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        #Extraer subtotal años sin descuento, para lo años con descuento mejor en la columa subtotal años
        'subtotal_years_sd': deudas.subtotal_sin_des,
        #'subtotal' : deudas.subtotal_años,
        'impuesto_adicional' : deudas.impuesto_adicional,
        'recargo' : deudas.recargo,
        'multa' : deudas.multa,
        'estatus':deudas.estatus,
        'total' : deudas.total        
       }) 
    #ciclo for para extraer los datos del contribuyente
    for data in extraer_datos_contribuyente:
       lista.append({
           'clave_catastral':data.pk_fk_clave_catastral.clave_catastral,
           'apellido_paterno':data.pk_fk_clave_catastral.apaterno,
           'apellido_materno':data.pk_fk_clave_catastral.amaterno,
           'nombre':data.pk_fk_clave_catastral.nombre,
           'calle_s':data.calle,
           'num_int':data.num_int,
           'num_ext':data.num_ext,
           'colonia_f':data.col_fracc,
           'estado_fisico':est_fisico_predio,
           'tipo_predio':tipo_predio,
       })

    context = {
        'my_list': lista,
        'adeudos':lista_adeudos,
        'titulo_pag': 'PAGO DE PREDIAL',
    }   
    return render(request, "finanzas/pago-predial/datos_consultados_contribuyente_años_debe.html",context)

#FUNCION PARA ACTUALIZAR EL ESTATUS DE DESCUENTO PARA SOLICITAR 
def solicitar_descuento(request, dato):
 
    if request.method == 'GET':
        años_seleccionados = request.GET.getlist('años[]')
        clave = request.GET.get('clave')
        estatus = request.GET.get('estatus')
        # Realiza las operaciones necesarias con los años seleccionados
        # ... 
        for año in años_seleccionados:
           resultado = models_finanzas.historial_pagos.objects.filter(contribuyente=clave.strip(), ejercicio=año.strip(),estatus=estatus.strip())
           for info in resultado:
               print(info.contribuyente.clave_catastral, ", ", info.estatus, ", ", info.ejercicio)                
               info.aplica_descuento = 'SOLICITADO'
               info.cajero = request.user.username
               clave_cat_contrib = info.contribuyente.clave_catastral
               info.save()
        
        #MANDAR NOTIFICACION A LA CONTADORA
        titulo = 'SOLICITUD DE DESCUENTO'
        cuerpo = f'Clave Catastral: {clave_cat_contrib}, Años solicitados: {años_seleccionados}'

        send_notify(request.user.username,'sup_fin',titulo, cuerpo)
        
        # Mandar correo
        
           
        # Devuelve una respuesta JSON
        return JsonResponse({'mensaje': 'Años recibidos con éxito.'})
    
#FUNCIÓN QUE HABILITA LA PANTALLA DEUDOR DEPENDIENDO SI VA AL CORRIENTE O DEBE MAS DE 1 AÑO

def busqueda_valida_adeudos(request, dato):
    adeudos = models_finanzas.historial_pagos.objects.filter(contribuyente=dato, estatus='NO PAGADO').count()
    if adeudos>1:
       return pago_predial_datos_2(request, dato)
    else:
       return pago_predial_datos_1(request, dato)

#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def pantalla_seleccion_cajera(request):
    ctx={
        'titulo_pag':'DESCUENTOS APROBADOS'
    }
    return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html",ctx)


def pantalla_seleccion_cajera(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models_finanzas.historial_pagos.objects.filter(aplica_descuento='APROBADO')

    if(adeudos_contribuyentes.exists()==True):

        for i in adeudos_contribuyentes:
         años.append({
            'años':i.ejercicio
         })

        for datos in adeudos_contribuyentes:
         dat.append({
            'clave':datos.contribuyente.clave_catastral,
            'nombre':datos.contribuyente.nombre,
            'apaterno':datos.contribuyente.apaterno,
            'amaterno':datos.contribuyente.amaterno,
            'años':datos.ejercicio
         })
        
        for elemento in dat:
            clave = elemento['clave']
            if clave in claves:
                for item in lista_duplicados:
                    if item['clave'] == clave:
                        item['años'] += ',' + elemento['años']
                        break
            else:
                claves.add(clave)
                lista_duplicados.append(elemento)
                
       
        return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html",{'años':años, 'dat':lista_duplicados, 'titulo_pag':'DESCUENTOS APROBADOS'})
    else:
        return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html" , {'titulo_pag':'DESCUENTOS APROBADOS'})


#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def pantalla_seleccion_contadora(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models_finanzas.historial_pagos.objects.filter(aplica_descuento='SOLICITADO')

    if(adeudos_contribuyentes.exists()==True):

        for i in adeudos_contribuyentes:
         años.append({
            'años':i.ejercicio
         })

        for datos in adeudos_contribuyentes:
         dat.append({
            'clave':datos.contribuyente.clave_catastral,
            'nombre':datos.contribuyente.nombre,
            'apaterno':datos.contribuyente.apaterno,
            'amaterno':datos.contribuyente.amaterno,
            'años':datos.ejercicio
         })
        
        for elemento in dat:
            clave = elemento['clave']
            if clave in claves:
                for item in lista_duplicados:
                    if item['clave'] == clave:
                        item['años'] += ',' + elemento['años']
                        break
            else:
                claves.add(clave)
                lista_duplicados.append(elemento)
                
       
        return render(request,"finanzas/pago-predial/descuentos/index-aplicar-descuentos.html",{'años':años, 'dat':lista_duplicados, 'titulo_pag': 'APLICAR DESCUENTOS PAGO PREDIAL'})
    else:
        return render(request,"finanzas/pago-predial/descuentos/index-aplicar-descuentos.html",{'titulo_pag': 'APLICAR DESCUENTOS PAGO PREDIAL'})

#APLICAR DESCUENTOS USUARIO ADMINISTRADOR
def aplicar_descuentos_1(request,dato):
    return render(request,"finanzas/pago-predial/descuentos/aplicar-descuento-contribuyente.html")

#VISTA DONDE LA ADMINISTRADORA APLIA LOS DESCUENTOS
def aplicar_descuentos(request,dato):
    lista = []
    lista_adeudos =[]
    est_fisico_predio = ''
    tipo_predio = ''
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 

    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    pagos_adeudo = models_finanzas.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO') & Q(aplica_descuento='SOLICITADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        #'subtotal' : deudas.subtotal_años,
        'subtotal' : deudas.subtotal_sin_des,
        'impuesto_adicional' : deudas.impuesto_adicional,
        'recargo' : deudas.recargo,
        'multa' : deudas.multa,
        'estatus':deudas.estatus,
        'total' : deudas.total        
       }) 
    #ciclo for para extraer los datos del contribuyente
    for data in extraer_datos_contribuyente:
       lista.append({
           'clave_catastral':data.pk_fk_clave_catastral.clave_catastral,
           'apellido_paterno':data.pk_fk_clave_catastral.apaterno,
           'apellido_materno':data.pk_fk_clave_catastral.amaterno,
           'nombre':data.pk_fk_clave_catastral.nombre,
           'calle_s':data.calle,
           'num_int':data.num_int,
           'num_ext':data.num_ext,
           'colonia_f':data.col_fracc,
           'estado_fisico':est_fisico_predio,
           'tipo_predio':tipo_predio,   
       })

    context = {'my_list': lista, 'adeudos':lista_adeudos, 'titulo_pag': 'APLICAR DESCUENTOS PAGO PREDIAL',}   
    return render(request, "finanzas/pago-predial/descuentos/aplicar-descuento-contribuyente.html",context)

# PAGO PREDIAL CON DESCUENTO APLICADO
def view_pago_descuentos_aplicados(request,dato):
    lista = []
    lista_adeudos =[]
    est_fisico_predio = ''
    tipo_predio = ''
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 

    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    pagos_adeudo = models_finanzas.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO') & Q(aplica_descuento='APROBADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        'subtotal' : deudas.subtotal_sin_des,
        'subtotal_con_descuento' : deudas.subtotal_años,
        'impuesto_adicional' : deudas.impuesto_adicional,
        'recargo' : deudas.recargo,
        'desc_recargo' : deudas.descuento_recargo,
        'multa' : deudas.multa,
        'desc_multa' : deudas.descuento_multa,
        'estatus':deudas.estatus,
        'total' : deudas.total        
       }) 
    #ciclo for para extraer los datos del contribuyente
    for data in extraer_datos_contribuyente:
       lista.append({
           'clave_catastral':data.pk_fk_clave_catastral.clave_catastral,
           'apellido_paterno':data.pk_fk_clave_catastral.apaterno,
           'apellido_materno':data.pk_fk_clave_catastral.amaterno,
           'nombre':data.pk_fk_clave_catastral.nombre,
           'calle_s':data.calle,
           'num_int':data.num_int,
           'num_ext':data.num_ext,
           'colonia_f':data.col_fracc,
           'estado_fisico':est_fisico_predio,
           'tipo_predio':tipo_predio,
       })

    context = {'my_list': lista, 'adeudos':lista_adeudos, 'titulo_pag': 'PAGO DE PREDIAL DESCUENTOS APLICADOS',}   
    return render(request, "finanzas/pago-predial/descuentos/pago-descuento-aplicado.html",context)


def notificaciones_contabilizar(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models_finanzas.historial_pagos.objects.filter(aplica_descuento='SOLICITADO')

    if(adeudos_contribuyentes.exists()==True):

        for i in adeudos_contribuyentes:
         años.append({
            'años':i.ejercicio
         })

        for datos in adeudos_contribuyentes:
         dat.append({
            'clave':datos.contribuyente.clave_catastral,
            'nombre':datos.contribuyente.nombre,
            'apaterno':datos.contribuyente.apaterno,
            'amaterno':datos.contribuyente.amaterno,
            'años':datos.ejercicio
         })
        
        for elemento in dat:
            clave = elemento['clave']
            if clave in claves:
                for item in lista_duplicados:
                    if item['clave'] == clave:
                        item['años'] += ',' + elemento['años']
                        break
            else:
                claves.add(clave)
                lista_duplicados.append(elemento)
        
        data = {
        'cantidad_elementos': len(lista_duplicados)
        }
    
        return JsonResponse(data)
    else:
        return JsonResponse({'contador': 0})

def descuento_aprobado(request):
    #GUARDAR EN VARIABLES TODOS LOS ELEMENTOS TRAIDOS POR EL AJAX
    if request.method == 'GET':
        clave_cat = request.GET.get('clave_cat')
        porcentaje_recargo_condonado = request.GET.get('recargo_condonado')
        porcentaje_multa_condonado = request.GET.get('multa_condonado')
        total_con_descuento = request.GET.get('total_con_descuento')
    
        #RECORDATORIO PARA PONER BLOQUE DE CODIGO EN CASO DE QUE ESTEN APROBADOS LOS ADEUDOS
        
        #QUERY PARA OBTENER TODOS LOS ADEUDOS SOLICITADOS A UN CONTRIBUYETNTE
        query_historial_pagos = models_finanzas.historial_pagos.objects.filter(contribuyente = clave_cat, estatus = 'NO PAGADO', aplica_descuento='SOLICITADO' )
        
        #RECORRER RESULTADOS
        for rs_hp in query_historial_pagos:
            cajero = rs_hp.cajero
            rs_hp.total = total_con_descuento
            rs_hp.descuento_recargo = porcentaje_recargo_condonado
            rs_hp.descuento_multa = porcentaje_multa_condonado
            rs_hp.aplica_descuento = 'APROBADO'
            rs_hp.autorizacion = 'AUTORIZADO'
            rs_hp.save()        

        
    #MANDAR NOTIFICACION AL CAJERO DEL DESCUENTO APROBADO
    remitente = request.user.username
    send_notify(remitente, cajero, 'SOLICITUD DE DESCUENTO APROBADA', f'{remitente} aprobo la solicitud de descuento correspondiente a la clave catastral: {clave_cat}')
        
    return JsonResponse({'mensaje': 'descuento aprobado con exito'})
    
    #Mandar notificacion de aprobacion de descuento

def descuento_rechazado(request):
    if request.method == 'GET':
        clave_cat = request.GET.get('clave_cat')
        query_historial_pagos = models_finanzas.historial_pagos.objects.filter(contribuyente = clave_cat, estatus = 'NO PAGADO', aplica_descuento='SOLICITADO' )
        #RECORRER RESULTADOS
        for rs_hp in query_historial_pagos:
            #ACTUALIZAR EL CAMPO DE APLICA_DESCUENTO DE SOLICITADO A APROBADO
            cajero = rs_hp.cajero
            rs_hp.aplica_descuento = 'RECHAZADO'
            rs_hp.save()        

    #MANDAR NOTIFICACION AL CAJERO DEL DESCUENTO APROBADO
    remitente = request.user.username
    send_notify(remitente, cajero, 'SOLICITUD DE DESCUENTO RECHAZADA', f'{remitente} rechazo la solicitud de descuento correspondiente a la clave catastral: {clave_cat}')
        
    return JsonResponse({'mensaje': 'descuento rechazado con exito'})   


def pago_predial_contribuyente(request):
    if request.method == 'GET':
        clave_cat = request.GET.get('clave_cat')
        total = request.GET.get('total')
        years_selected = request.GET.getlist('years_selected[]')
        resumen_pago = request.GET.getlist('resumen_pago[]')
    
    # Convertir lista a cadena
    selecccion = str(years_selected)
    years_seleccionados= selecccion.replace('[','').replace(']','').replace("'","")


    query_historial_pagos = models_finanzas.historial_pagos.objects.filter(Q(contribuyente=clave_cat) & Q(estatus = 'NO PAGADO') & Q(autorizacion = 'AUTORIZADO') | Q(aplica_descuento='APROBADO'))
    # query_historial_pagos = models_finanzas.historial_pagos.objects.filter(contribuyente = clave_cat, estatus = 'NO PAGADO', aplica_descuento='APROBADO', autorizacion = 'AUTORIZADO')

    for rs_hp in query_historial_pagos:
        folio=rs_hp.folio
        
        # Eliminar los registros de folio para juntarlos en uno unico
        print('Se elimino el folio: '+ folio)
        query_historial_pagos.delete()
    
    lista_resumen_pago_float = []
    for i in resumen_pago:
        valor_float = float(i)
        lista_resumen_pago_float.append(valor_float)
    
    print(lista_resumen_pago_float)
    #print(f'subtotal: {resumen_pago[0]}')
    
    
    # Obtener el numero de folio
    folio_list = re.findall(r'\d+', folio)
    str_folio = str(folio_list)
    num_folio = str_folio.replace('[','').replace(']','').replace("'","")
    
    # Contribuyente que pasara como llave foranea
    contribuyente=models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    
    models_finanzas.historial_pagos.objects.create(
        folio = num_folio,contribuyente= contribuyente,
        ejercicio = years_seleccionados,
        subtotal_años  = lista_resumen_pago_float[0],
        impuesto_adicional = lista_resumen_pago_float[1],
        recargo = lista_resumen_pago_float[3],
        descuento_recargo = lista_resumen_pago_float[2],
        multa = lista_resumen_pago_float[5],
        descuento_multa = lista_resumen_pago_float[4],
        aplica_descuento = 'APROBADO',
        total=total,
        estatus = 'PAGADO',
        autorizacion='AUTORIZADO',
        cajero = request.user.username
    )
    
    # GENERAR REPORTE
    reporte_pago_predial_ad(request.user.username,clave_cat)

    return JsonResponse({'mensaje': 'pago exitoso'})

def pago_predial_contribuyente_years_corriente(request):
    
    if request.method == 'GET':
        folio = request.GET.get('folio')
        clave_cat = request.GET.get('clave_cat')
        concepto = request.GET.get('concepto')
        subtotal = request.GET.get('subtotal')
        contrib_adi = request.GET.get('contrib_adi')
        total = request.GET.get('total')
        observaciones = request.GET.get('observaciones')
        
    print('La clave catastral es: '+clave_cat)
    # Contribuyente que pasara como llave foranea
    contribuyente=models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    
    date = datetime.datetime.now()
    
    year = date.year
    
    models_finanzas.historial_pagos.objects.create(
        folio = folio,contribuyente= contribuyente,
        ejercicio = year,
        subtotal_años  = subtotal,
        impuesto_adicional = contrib_adi,
        recargo = 0,
        descuento_recargo = 0,
        multa = 0,
        descuento_multa = 0,
        aplica_descuento = 'NO APLICA',
        total=total,
        estatus = 'PAGADO',
        autorizacion='AUTORIZADO',
        cajero = request.user.username
    )
    
    reporte_pago_predial_corriente(folio,concepto,clave_cat,request.user.username,observaciones)
    
    
    return JsonResponse ({'mensaje': 'pago exitoso'})



