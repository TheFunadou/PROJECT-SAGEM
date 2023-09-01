from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from notify.models import notify as notify_finanzas
from django.contrib.auth.models import User

from catastro import models

from catastro.models import Datos_Contribuyentes, Domicilio_inmueble

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

# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')

#Obtener username como objecto tipo user
def obtener_username(request):
    nom_user = request.user.username
    
    obj_user = User.objects.get(username= nom_user)
    
    return obj_user
    
    

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
                return redirect('catastro:perfil_su')
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
        'titulo_pag': 'INICIO SUPER USUARIO FINANZAS',
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
## <<< APARTADO DE FINANZAS PAGO PREDIAL>>> ##


## --- EL CONTRIBUYENTE VA AL CORRIENTE

#PANTALLA PARA BUSQUEDA DEL CONTRIBUYENTE 
def buscar_adeudos(request):
    return render(request, "finanzas/pago-predial/busqueda_contribuyente_1.html")

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

    datos_predios = models.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

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

    datos_predios = models.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    pagos_adeudo = models.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        'subtotal' : deudas.subtotal_años,
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
           'tipo_predio':tipo_predio
            
       })

    context = {'my_list': lista, 'adeudos':lista_adeudos}   
    return render(request, "finanzas/pago-predial/datos_consultados_contribuyente_años_debe.html",context)

#FUNCION PARA ACTUALIZAR EL ESTATUS DE DESCUENTO PARA SOLICITAR 
def solicitar_descuento(request,dato):
 
    if request.method == 'GET':
        años_seleccionados = request.GET.getlist('años[]')
        clave = request.GET.get('clave')
        estatus = request.GET.get('estatus')
        # Realiza las operaciones necesarias con los años seleccionados
        # ... 
        for año in años_seleccionados:
           resultado = models.historial_pagos.objects.filter(contribuyente=clave.strip(), ejercicio=año.strip(),estatus=estatus.strip())
           for info in resultado:
               print(info.contribuyente.clave_catastral, ", ", info.estatus, ", ", info.ejercicio)
               info.aplica_descuento = 'SOLICITADO'
               info.save()
           
        # Devuelve una respuesta JSON
        return JsonResponse({'mensaje': 'Años recibidos con éxito.'})
    
#FUNCIÓN QUE HABILITA LA PANTALLA DEUDOR DEPENDIENDO SI VA AL CORRIENTE O DEBE MAS DE 1 AÑO

def busqueda_valida_adeudos(request, dato):
    adeudos = models.historial_pagos.objects.filter(contribuyente=dato, estatus='NO PAGADO').count()
    if adeudos>1:
       return pago_predial_datos_2(request, dato)
    else:
       return pago_predial_datos_1(request, dato)

#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def pantalla_seleccion_cajera(request):

    return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html")


def pantalla_seleccion_cajera(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models.historial_pagos.objects.filter(aplica_descuento='APROBADO')

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
                
       
        return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html",{'años':años, 'dat':lista_duplicados})
    else:
        return render(request,"finanzas/pago-predial/descuentos/index-descuentos-aplicados.html")


#PANTALLA PARA CONSULTAS DE CONTRIBUYENTES CON DEUDA
def pantalla_seleccion_contadora(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models.historial_pagos.objects.filter(aplica_descuento='SOLICITADO')

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
                
       
        return render(request,"finanzas/pago-predial/descuentos/index-aplicar-descuentos.html",{'años':años, 'dat':lista_duplicados})
    else:
        return render(request,"finanzas/pago-predial/descuentos/index-aplicar-descuentos.html")

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

    datos_predios = models.Datos_inmuebles.objects.filter(fk_clave_catastral = dato)

    pagos_adeudo = models.historial_pagos.objects.filter(Q(contribuyente=dato) & Q(estatus='NO PAGADO') & Q(aplica_descuento='SOLICITADO')).order_by('ejercicio')

    for predio in datos_predios:
        est_fisico_predio = predio.pk_estado_fisico_predio
        tipo_predio = predio.tipo_predio

    #ciclo for para extraer datos de adeudos
    for deudas in pagos_adeudo:
       lista_adeudos.append({
        'clave':deudas.contribuyente.clave_catastral,
        'ejercicio' : deudas.ejercicio,
        'subtotal' : deudas.subtotal_años,
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
           'tipo_predio':tipo_predio
            
       })

    context = {'my_list': lista, 'adeudos':lista_adeudos}   
    return render(request, "finanzas/pago-predial/descuentos/aplicar-descuento-contribuyente.html",context)


def notificaciones_contabilizar(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models.historial_pagos.objects.filter(aplica_descuento='SOLICITADO')

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

def redireccionar_menu_su(request,dato):
 
        
    resultado = models.historial_pagos.objects.filter(contribuyente=dato, estatus='NO PAGADO',aplica_descuento='SOLICITADO')
    for info in resultado:
        print(info.contribuyente.clave_catastral, ", ", info.estatus, ", ", info.ejercicio)
        info.aplica_descuento = 'APROBADO'
        info.save()
           
        # Devuelve una respuesta JSON
    return redirect('finanzas:perfil_su_fin')         
       
def notificaciones_contabilizar_cajera(request):
    años =[]
    dat = []
    lista_duplicados = []
    claves = set()
    adeudos_contribuyentes = models.historial_pagos.objects.filter(aplica_descuento='APROBADO')

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



#REDIRECCIONA AL MENU PRINCIPAL
def redireccionar_menu(request):
    return redirect('finanzas:perfil_fin')





    




