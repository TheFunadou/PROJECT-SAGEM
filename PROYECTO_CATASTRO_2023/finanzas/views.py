from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.db.models import Sum, Max
from django.db import transaction, IntegrityError
from django.urls import *
from django.utils import timezone
from notify.models import notify as notify_finanzas
from django.contrib.auth.models import User

from catastro import models as models_catastro
from finanzas import models as models_finanzas
from catastro.models import Domicilio_inmueble

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

from .reports.reporte_pago_predial import reporte_pago_predial
from .reports.reporte_pago_predial_c import reporte_pago_predial_corriente

#reportes

import datetime
from catastro import models as models_cat
from finanzas import models as models_fin
from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
import json
import os
from catastro import functions
from num2words import num2words
from report.report import report


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
        # 'titulo_pag': f'BIENVENIDO {request.user.username}',
        'titulo_pag': 'INICIO CONTADORA',
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
    return render(request, "finanzas/pago-predial/busqueda_contribuyente_1.html",{'titulo_pag': 'PAGO PREDIAL: BUSQUEDA DE CONTRIBUYENTE'})

#FUNCIÓN QUE HABILITA LA PANTALLA DEUDOR DEPENDIENDO SI VA AL CORRIENTE O DEBE MAS DE 1 AÑO

def busqueda_valida_adeudos(request, dato):
    adeudos = models_finanzas.pago_predial.objects.filter(contribuyente=dato, estatus='NO PAGADO').count()
    if adeudos>0:
        # El contribuyente tiene adeudos
    #    return view_pago_predial_adeudos(request, dato)
        return view_pago_predial(request,True, dato)
    else:
        # El contribuyente tiene pagos al corriente
        # return pago_predial_datos_1(request, dato)
        return view_pago_predial(request,False, dato)


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

"""#CONSULTA DE DATOS DEL CONTRIBUYENTE PARA MOSTRAR EN LA PANTALLA DE PAGO DE PREDIO
def pago_predial_datos_1(request,dato):
    lista = []
    lista_adeudos = []
    est_fisico_predio = ''
    tipo_predio = ''
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 
    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)
    #    Adeudos contribuyente
    query_adeudos = models_finanzas.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in query_adeudos:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        #Extraer subtotal años sin descuento, para lo años con descuento mejor en la columa subtotal años
        'subtotal_years_sd': deudas.subtotal_años,
        #'subtotal' : deudas.subtotal_años,
        'impuesto_adicional' : deudas.impuesto_adicional,
        'recargo' : deudas.recargo,
        'multa' : deudas.multa,
        'estatus':deudas.estatus,
        'total' : deudas.total        
       }) 

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
       

    return render(request,"finanzas/pago-predial/datos_consultados_contribuyente_1.html",{'nom_pag': 'INGRESOS', 'titulo_pag': 'PAGO DE IMPUESTO PREDIAL', 'my_list': lista,'adeudos':lista_adeudos})

"""
# --- CONTRIBUYENTE DEBE AÑOS

#PANTALLA PARA BUSQUEDA DEL CONTRIBUYENTE 
def pago_predial_busqueda_2(request):
    return render(request, "finanzas/pago-predial/busqueda_contribuyente_2.html")

# Si estatus = True es son años mayores a 0, si es False va con pago al corriente
#CONSULTA DE DATOS DEL CONTRIBUYENTE PARA MOSTRAR EN LA PANTALLA DE PAGO DE PREDIO
def view_pago_predial(request, estatus ,contribuyente):
    contribuyente_data_list = []
    adeudos_data_list =[]
    est_fisico_predio = ''
    tipo_predio = ''
    datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = contribuyente))
    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = contribuyente)
    fk_contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=contribuyente)
    adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente_id = fk_contribuyente)  &  (Q(estatus='NO PAGADO') | Q(folio = 0))).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for data in adeudos:
       adeudos_data_list.append({
        'clave_cat':data.contribuyente.clave_catastral,
        'ejercicio' : data.ejercicio,
        'impuesto_predial': "{:,.2f}".format(data.impuesto_predial),
        'impuesto_adicional' : "{:,.2f}".format(data.impuesto_adicional),
        'recargo' : "{:,.2f}".format(data.recargo),
        'multa' : "{:,.2f}".format(data.multa),
       })
       print(f'clave_cat: {data.contribuyente.clave_catastral}, ejercicio: {data.ejercicio}')
       
    #ciclo for para extraer los datos del contribuyente
    for data in datos_contribuyente:
       contribuyente_data_list.append({
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
       
    if estatus == True:
        # El contribuyente tiene adeudos
        return render(request, "finanzas/pago-predial/pago_predial_adeudos.html", {'my_list': contribuyente_data_list, 'adeudos':adeudos_data_list, 'titulo_pag': 'PAGO PREDIAL'})
    else:
        # El contribuyente tiene sus pago al corriente
        return HttpResponse('Pagos al corriente ,Ok')
    
"""
#CONSULTA DE DATOS DEL CONTRIBUYENTE PARA MOSTRAR EN LA PANTALLA DE PAGO DE PREDIO
def pago_predial_datos_2(request,contribuyente):
    contribuyente_data_list = []
    adeudos_data_list =[]
    est_fisico_predio = ''
    tipo_predio = ''
    datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = contribuyente))
    datos_predios = models_catastro.Datos_inmuebles.objects.filter(fk_clave_catastral = contribuyente)
    fk_contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=contribuyente)
    adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente=fk_contribuyente) & Q(estatus='NO PAGADO') | Q(folio = 0) ).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for data in adeudos:
       adeudos_data_list.append({
        'clave_cat':data.contribuyente.clave_catastral,
        'ejercicio' : data.ejercicio,
        'impuesto_predial': data.impuesto_predial,
        'impuesto_adicional' : data.impuesto_adicional,
        'recargo' : data.recargo,
        'multa' : data.multa,
       })
       
    #ciclo for para extraer los datos del contribuyente
    for data in datos_contribuyente:
       contribuyente_data_list.append({
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

    return render(request, "finanzas/pago-predial/pago_predial_adeudos.html", {'my_list': contribuyente_data_list, 'adeudos':adeudos_data_list, 'titulo_pag': 'PAGO DE PREDIAL'})


"""

#FUNCION PARA ACTUALIZAR EL ESTATUS DE DESCUENTO PARA SOLICITAR 
def solicitar_descuento(request):
    try:
        if request.method == 'GET':
            years_selected_list = request.GET.getlist('years_selected[]')
            clave_cat = request.GET.get('clave_cat')
        # Quitar corchetes de la lista
        years_selected = ', '.join(map(str, years_selected_list))
        # Realiza las operaciones necesarias con los años seleccionados
        contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
        query_adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente=contribuyente) & (Q(estatus = 'NO PAGADO') | Q(folio=0))  & Q(autorizacion = 'AUTORIZADO') & Q(estatus_descuento = 'NO SOLICITADO') & Q(ejercicio__in=years_selected_list))
        
        with transaction.atomic():
            for rs in query_adeudos:
                rs.estatus_descuento = 'SOLICITADO'
                rs.cajero = request.user.username
                rs.fecha_hora = timezone.now()
                rs.save()
            #MANDAR NOTIFICACION A LA CONTADORA
            send_notify(request.user.username,'contadora','SOLICITUD DE DESCUENTO', f'Clave Catastral: {clave_cat}, Años solicitados: {years_selected_list}')
    except IntegrityError:
        print('ERROR AL SOLICITAR DESCUENTO')
    transaction.commit()
    # Devuelve una respuesta JSON
    return JsonResponse({'years_selected': years_selected})

#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def pantalla_seleccion_cajera(request):
    return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html",{'titulo_pag':'PAGO PREDIAL: SELECCION DE DESCUENTOS APROBADOS'})

############

#PANTALLA CAJERO PARA SELECCION DE DESCUENTOS APROBADOS
def view_seleccion_descuentos_aprobados(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    # adeudos_contribuyentes = models_finanzas.pago_predial.objects.filter(estatus_descuento='APROBADO').order_by('fecha_hora')[:10]
    adeudos_contribuyentes = models_finanzas.pago_predial.objects.filter(Q(cajero = request.user.username) & (Q(estatus='NO PAGADO') | Q(folio = 0)) & Q(estatus_descuento='APROBADO')).order_by('ejercicio')[:10]

    if adeudos_contribuyentes.exists():

        for i in adeudos_contribuyentes:
         años.append({
            'years':i.ejercicio
         })

        for datos in adeudos_contribuyentes:
         dat.append({
            'clave_cat':datos.contribuyente.clave_catastral,
            'nombre_completo': f'{datos.contribuyente.nombre} {datos.contribuyente.apaterno} {datos.contribuyente.amaterno}',
            'years':datos.ejercicio,
            'fecha_hora':datos.fecha_hora,
        })
        
        for elemento in dat:
            clave = elemento['clave_cat']
            if clave in claves:
                for item in lista_duplicados:
                    if item['clave_cat'] == clave:
                        item['years'] += ',' + elemento['years']
                        break
            else:
                claves.add(clave)
                lista_duplicados.append(elemento)
        
        return render(request,"finanzas/pago-predial/descuentos/seleccion_descuentos_aprobados.html",{'años':años, 'dat':lista_duplicados, 'titulo_pag': 'PAGO PREDIAL: SELECCION DE DESCUENTOS APROBADOS'})
    else:
        return render(request,"finanzas/pago-predial/descuentos/seleccion_descuentos_aprobados.html",{'titulo_pag': 'PAGO PREDIAL: SELECCION DE DESCUENTOS APROBADOS'})


###########


#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def view_seleccion_descuentos_solicitados(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models_finanzas.pago_predial.objects.filter(estatus_descuento='SOLICITADO').order_by('fecha_hora')[:10]

    if adeudos_contribuyentes.exists():

        for i in adeudos_contribuyentes:
         años.append({
            'years':i.ejercicio
         })

        for datos in adeudos_contribuyentes:
         dat.append({
            'clave_cat':datos.contribuyente.clave_catastral,
            'nombre_completo': f'{datos.contribuyente.nombre} {datos.contribuyente.apaterno} {datos.contribuyente.amaterno}',
            'years':datos.ejercicio,
            'fecha_hora':datos.fecha_hora,
            'cajero':datos.cajero
        })
        
        for elemento in dat:
            clave = elemento['clave_cat']
            if clave in claves:
                for item in lista_duplicados:
                    if item['clave_cat'] == clave:
                        item['years'] += ',' + elemento['years']
                        break
            else:
                claves.add(clave)
                lista_duplicados.append(elemento)
        
        return render(request,"finanzas/pago-predial/descuentos/seleccion_solicitudes_descuento.html",{'años':años, 'dat':lista_duplicados, 'titulo_pag': 'PAGO PREDIAL: SOLICITUDES DE DESCUENTO'})
    else:
        return render(request,"finanzas/pago-predial/descuentos/seleccion_solicitudes_descuento.html",{'titulo_pag': 'PAGO PREDIAL: SELECCION DE SOLICITUDES DE DESCUENTO'})

#APLICAR DESCUENTOS USUARIO ADMINISTRADOR
def aplicar_descuentos_1(request,dato):
    return render(request,"finanzas/pago-predial/descuentos/aplicar-descuento-contribuyente.html")


#VISTA DONDE LA ADMINISTRADORA APLICA LOS DESCUENTOS
def aplicar_descuentos(request,dato):
    lista = []
    lista_adeudos =[]
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 
    datos_predios = models_catastro.Datos_inmuebles.objects.get(fk_clave_catastral = dato)
    pagos_adeudo = models_finanzas.pago_predial.objects.filter(Q(contribuyente=dato) & (Q(estatus='NO PAGADO') | Q(folio = 0)) & Q(estatus_descuento='SOLICITADO')).order_by('ejercicio')

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        'impuesto_predial' : "{:,.2f}".format(deudas.impuesto_predial),
        'impuesto_adicional' : "{:,.2f}".format(deudas.impuesto_adicional),
        'recargo' : "{:,.2f}".format(deudas.recargo),
        'multa' : "{:,.2f}".format(deudas.multa),
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
           'estado_fisico':datos_predios.pk_estado_fisico_predio,
           'tipo_predio':datos_predios.tipo_predio,   
       })
    return render(request, "finanzas/pago-predial/descuentos/aprobar_descuento.html",{'my_list': lista, 'adeudos':lista_adeudos, 'titulo_pag': 'PAGO PREDIAL: APROBAR DESCUENTOS'})

# PAGO PREDIAL CON DESCUENTO APLICADO
def view_pago_descuento_aprobado(request,dato):
    lista = []
    lista_adeudos =[]
    extraer_datos_contribuyente = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral = dato)) 
    datos_predios = models_catastro.Datos_inmuebles.objects.get(fk_clave_catastral = dato)
    pagos_adeudo = models_finanzas.pago_predial.objects.filter(Q(contribuyente=dato) & (Q(estatus='NO PAGADO') | Q(folio = 0)) & Q(estatus_descuento='APROBADO')).order_by('ejercicio')

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        'impuesto_predial' : "{:,.2f}".format(deudas.impuesto_predial),
        'impuesto_adicional' : "{:,.2f}".format(deudas.impuesto_adicional),
        'recargo' : "{:,.2f}".format(deudas.recargo),
        'desc_recargo' : "{:,.2f}".format(deudas.desc_recargo),
        'multa' : "{:,.2f}".format(deudas.multa),
        'desc_multa' : "{:,.2f}".format(deudas.desc_multa),
        'total_descuento': "{:,.2f}".format(deudas.descuento),
        'total_sd': "{:,.2f}".format(deudas.total)
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
           'estado_fisico':datos_predios.pk_estado_fisico_predio,
           'tipo_predio':datos_predios.tipo_predio,   
       })
    return render(request, "finanzas/pago-predial/descuentos/pago_descuento_aprobado.html",{'my_list': lista, 'adeudos':lista_adeudos, 'titulo_pag': 'PAGO PREDIAL: PAGO DESCUENTO APROBADO'})

def descuento_aprobado(request):
    try:
        if request.method == 'GET':
            clave_cat = request.GET.get('clave_cat')
            desc_recargo = request.GET.get('desc_recargo')
            desc_multa = request.GET.get('desc_multa')
            descuento_total = request.GET.get('descuento_total')
            years_selected_list = request.GET.getlist('years_selected[]')
            total_sd = request.GET.get('total_sd','0')
            
        print(f'total sin descuento: {total_sd}')
        years_selected = ', '.join(map(str, years_selected_list))
        contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
        query_adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente=contribuyente) & (Q(estatus = 'NO PAGADO') | Q(folio=0))  & Q(autorizacion = 'AUTORIZADO') & Q(ejercicio__in=years_selected_list))
        
        with transaction.atomic():
            for rs in query_adeudos:
                rs.estatus_descuento = 'APROBADO'
                rs.desc_recargo = desc_recargo
                rs.desc_multa = desc_multa
                rs.descuento = descuento_total
                rs.total = total_sd
                rs.fecha_hora = timezone.now()
                #guardar cambios
                rs.save()
                cajero = rs.cajero
                  
            send_notify(request.user.username, cajero , 'SOLICITUD DE APROBADA', f'{request.user.username} aprobo la solicitud de descuento correspondiente a la clave catastral: {clave_cat}')
            
    except IntegrityError:
        print('ERROR AL REALIZAR LA TRANSACCION DE APROBAR DESCUENTO')
    transaction.commit()
    return JsonResponse({'years_selected': years_selected})   

def descuento_rechazado(request):
    try:
        if request.method == 'GET':
            clave_cat = request.GET.get('clave_cat')
            years_selected_list = request.GET.getlist('years_selected[]')
        years_selected = ', '.join(map(str, years_selected_list))
        contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
        query_adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente=contribuyente) & (Q(estatus = 'NO PAGADO') | Q(folio=0))  & Q(autorizacion = 'AUTORIZADO') & Q(ejercicio__in=years_selected_list))
        
        with transaction.atomic():
            for rs in query_adeudos:
                rs.estatus_descuento = 'RECHAZADO'
                rs.fecha_hora = timezone.now()
                #guardar cambios
                rs.save()
                cajero = rs.cajero
                  
            send_notify(request.user.username, cajero , 'SOLICITUD RECHAZADA', f'Solicitud rechazada para el contribuyente: {clave_cat}, Años solicitados: {years_selected}')
    except IntegrityError:
        print('ERROR AL REALIZAR LA TRANSACCION DE RECHAZAR DESCUENTO')
    transaction.commit()
    return JsonResponse({'years_selected': years_selected})   


def pago_predial(request):         
    try:
        if request.method == 'GET':
            clave_cat = request.GET.get('clave_cat')
            impuesto_predial = request.GET.get('impuesto_predial')
            impuesto_adicional = request.GET.get('impuesto_adicional')
            recargo = request.GET.get('recargo',0)
            desc_recargo = request.GET.get('desc_recargo',0)
            multa = request.GET.get('multa',0)
            desc_multa = request.GET.get('desc_multa',0)
            total = request.GET.get('total')
            #Si no se obtiene ningun valor de la variable descuento del frontend entonces se asigna un valor por default
            descuento = request.GET.get('descuento',0)
            observaciones = request.GET.get('observaciones')
            estatus_descuento = request.GET.get('estatus_descuento','NO SOLICITADO')
            years_selected_list = request.GET.getlist('years_selected[]')
        
        contribuyente = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
        query_adeudos = models_finanzas.pago_predial.objects.filter(Q(contribuyente=contribuyente) & (Q(estatus = 'NO PAGADO') | Q(folio=0))  & Q(autorizacion = 'AUTORIZADO') & Q(ejercicio__in=years_selected_list))
        # Quitar corchetes de la lista
        years_selected = ', '.join(map(str, years_selected_list))
        # Obtener el ultimo folio
        max_folio = models_finanzas.pago_predial.objects.aggregate(max_folio=Max('folio'))['max_folio']
        # Folio nvo
        nvo_folio = max_folio + 1 if max_folio is not None else 1
        
        with transaction.atomic():
            query_adeudos.delete()
            # Dar de alta el registro de pago
            pay_data = models_finanzas.pago_predial.objects.create(
                folio = nvo_folio, contribuyente = contribuyente , ejercicio = years_selected, impuesto_predial = impuesto_predial, impuesto_adicional = impuesto_adicional, recargo = recargo, desc_recargo=desc_recargo, multa = multa , desc_multa=desc_multa, descuento = descuento , estatus_descuento = estatus_descuento, cajero = request.user.username , estatus = 'PAGADO', total = total, autorizacion = 'AUTORIZADO', fecha_hora = timezone.now()
            )
            #IMPIRMIR REPORTE DE PAGO
            # reporte_pago_predial(request.user.username,clave_cat,years_selected,pay_data.folio,observaciones)
    except IntegrityError:
       print('ERROR AL REALIZAR LA TRANSACCION DE PAGO')
    transaction.commit()
    return JsonResponse({'cajero': request.user.username,'clave_cat':clave_cat,'ejercicios':years_selected,'folio':pay_data.folio,'observaciones':observaciones})   

# ----------------------------- PAGO DERECHOS -----------------------#

def view_pago_derechos(request):
    return render(request,'finanzas/derechos/pago_derechos.html',{'titulo_pag':'PAGO DE DERECHOS'})

def search_derechos(request):
    if request.method == 'GET':
        id_derecho = request.GET.get('id_derecho')
    query_td = models_finanzas.tabla_derechos.objects.filter(id_derecho=id_derecho).values()
    # Convertir queryset a lista
    data = list(query_td) 
    return JsonResponse(data,safe=False)

def search_precio_derecho(request):
    if request.method == 'GET':
        nombre_derecho = request.GET.get('nombre_derecho')
    query_td = models_finanzas.tabla_derechos.objects.get(nombre_derecho=nombre_derecho)
    return JsonResponse({'precio':query_td.precio})


def pago_derecho(request):
    if request.method == 'GET':
        nombre= request.GET.get('nombre')
        observaciones = request.GET.get('observaciones')
        concepto=request.GET.get('concepto')
        cantidad=request.GET.get('cantidad')
        subtotal=request.GET.get('subtotal')
        descuento=request.GET.get('descuento')
        impuesto_adicional=request.GET.get('impuesto_adicional')
        total=request.GET.get('total')
        cajero = request.user.username
        
        
    
    return JsonResponse({'cajero':cajero,'nombre': nombre,'observaciones': observaciones,'concepto': concepto,'cantidad': cantidad,'subtotal': subtotal,'descuento': descuento,'impuesto_adicional': impuesto_adicional,'total': total})
    
