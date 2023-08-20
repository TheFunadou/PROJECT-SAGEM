from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from notify.models import notify as notify_finanzas
from django.contrib.auth.models import User
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