from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *

# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')


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
        'nom_pag': 'FINANZAS',
        'titulo_pag': 'INICIO FINANZAS',
        'nombre_user': request.user.username
    }
    
    return render(request,'finanzas/inicio_finanzas.html',ctx)


# PERFIL SUPERUSUARIO

@login_required(login_url="pag_login")
def perfil_sup_user_finanzas(request):
    
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
    
    ctx = {
        'nom_pag': 'FINANZAS',
        'titulo_pag': 'INICIO SUPER USUARIO FINANZAS',
        'nombre_user': request.user.username
    }

    return render(request, 'finanzas/inicio_sup_user_finanzas.html', ctx)