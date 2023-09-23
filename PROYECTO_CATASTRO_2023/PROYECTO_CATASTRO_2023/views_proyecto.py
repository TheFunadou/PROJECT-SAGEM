from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import *


# VIEWS DEL PROYECTO (NO CONFUNDIR CON LAS DE LAS APLICACIONES XD ESAS SON INDEPENDIENTES)

# SE MUESTRA LA PAGINA DE INICIO DE SESION PARA QUE EL USUARIO META SU USUARIO Y CONTRASENA Y POSTERIORMENTE SON ENVIADOS A LA VISTA INICIO_SESION

# PAGINA LOGIN
def pagina_login(request):
    # IF PARA REGRESAR AL USUARIO A SU PAGINA DE INICIO SI INTENTA REGRESAR AL LOGIN DE ACUERDO A SU GRUPO SI ESTA AUTENTICADO
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
    
    # SI EL USUARIO NO ESTA AUTENTICADO SE RENDERIZA LA PAGINA DE LOGIN
    else:
        # print("El usuario no esta autenticado")
        return render(request, 'registration/pantalla_inicio.html')
    
# VIEW PARA CERRAR SESION
def cerrar_sesion(request):
    logout(request)
    
    return redirect('pag_login')



# AUTENTICACION Y REDIRECCIONAMIENTO DE USUARIOS
def autenticacion(request):

    id_user = request.POST['username']
    user_pass = request.POST['password']

    # print(id_user)
    # print(user_pass)

    user = authenticate(request, username=id_user, password=user_pass)

    if user is not None:
        login(request, user)
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
        
        messages.error(request, 'Usuario o contraseña incorrecto. Ingrese los datos nuevamente.')
        return redirect('pag_login')

    