from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from django.utils import timezone
# CREATE VIEW PARA GENERAR UNA CLASE PARA GUARDAR DATOS
from django.views.generic import CreateView
from catastro import models

#TABLA USUARIOS
from django.contrib.auth.models import User
#DJANGO NOTIFICACIONS



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

# NOTIFICACIONES PRUEBA
def vista_prueba(request):
    
    return render (request,'catastro/prueba_notify.html')


""""
def enviar(request):
    id= request.POST['id']
    
    usuario_remtitente= User.objects.get(username=request.user.username)
    usuario_destino = User.objects.get(username=id)
    cuerpo= request.POST['cuerpo']
    cuerpo2= request.POST['cuerpo2']
    
    
    notify.send(usuario_remtitente, recipient=usuario_destino, verb=cuerpo,description=cuerpo2)
    
"""

def enviar(request):
    usuario_remtitente= User.objects.get(username=request.user.username)
    
    
    print('EL usuario remitente es: '+usuario_remtitente.notifications)
    

""""
class registrar_contribuyentes(CreateView):
    model = models.contribuyente
    fields = ['rfc', 'nombre', 'ap', 'am', 'telefono']
    template_name = 'catastro/alta_contribuyentes.html'
    form_class = ContribuyenteForm
    success_url = reverse_lazy('perfil_cat')  # Define la URL de redireccionamiento
"""

def menu_willy(request):
    return render(request,'catastro/menu_principal_willy.html')

# HFG
    
    
    
