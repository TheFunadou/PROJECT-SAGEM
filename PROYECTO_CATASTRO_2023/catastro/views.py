from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from django.utils import timezone
# CREATE VIEW PARA GENERAR UNA CLASE PARA GUARDAR DATOS
from django.views.generic import CreateView
from notify import models as notify_models
#TABLA USUARIOS
from django.contrib.auth.models import User, Group
#DJANGO NOTIFICACIONS

# channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')




# Create your views here.
@login_required(login_url="pag_login")
def perfil_catastro(request):
    
    #REDIRECCIONAR A USUARIO QUE NO PERTENEZCAN A ESE DEPARTAMENTO
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su_cat')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx={
        'url_pag': 'x',
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO CATASTRO'
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
                return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx = {
        'notficaciones':'Notification.objects.values("description").filter()',
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO SUPER USUARIO CATASTRO',
        'nombre_user': request.user.username
    }

    return render(request, 'catastro/inicio_sup_user_catastro.html', ctx)


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
    
    # Crear nuevo usuario
    new_user= User(username=username, email=email)
    new_user.set_password(conf_password)
    
    if(rol == 'STAFF'):
        new_user.save()
    elif(rol == 'SUPER_USUARIO'):
        new_user.is_superuser=True
        new_user.save()
    
    # Asginar un grupo al usuario
    usuario = User.objects.get(username=username)
    grupo = Group.objects.get(name=departamento)
    
    usuario.groups.add(grupo)
    
    
@login_required(login_url="pag_login")
def views_cambiar_password(request):
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
        'titulo_pag': 'RECUPERAR CONTRASEÑA'
    }
    
    return render(request, 'catastro/cambiar_password', ctx)


@login_required(login_url='pag_login')
def cambiar_password(request):
    username = request.POST['username']
    password = request.POST['password']
    conf_password = request.POST['conf_password']

def view_notify(request):
    return render(request,'catastro/notification_2.html')
    
def send_notify_test(request):

    remitente = request.user.username
    destinatario = request.POST['destinatario']
    id_dest = User.objects.get(username=destinatario)
    titulo = request.POST['titulo']
    cuerpo = request.POST['cuerpo']

    
    notify_models.notify.objects.create(
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
    
    
    return HttpResponse('Notificacion enviada')


    
    
    
