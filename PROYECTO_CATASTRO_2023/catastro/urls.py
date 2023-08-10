"""
URL configuration for PROYECTO_CATASTRO_2023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from catastro import views

app_name='catastro'

urlpatterns = [
    
    #CERRAR_SESION
    path('logout_catastro/', views.cerrar_sesion, name='logout_catastro'),
    #PERFIL USUARIO NORMAL
    path('perfil/',views.perfil_catastro, name='perfil_cat'),
    #PERFIL SUPER USUARIO
    path('perfil_su/',views.perfil_sup_user_catastro, name='perfil_su_cat'),
    path('view_registrar_usuario/',views.view_registrar_usuario, name='view_registrar_usuario'),
    path('view_cambiar_contra/', views.views_cambiar_password, name='view_cambiar_password'),
    
    
    # REGISTRAR NUEVOS CONTIBUYENTES
    #path('registro_contribuyente/',views.registrar_contribuyentes.as_view(), name='registro_contribuyente'),

    
    #RUTA PARA VISUALIZAR EL ALTA DE CIUDADANO O CONTRIBUYENTE
    path('catastro/perfil/registro_contribuyente/',views.contribuyente_index,name='vista_alta_contribuyente'),

    #RUTA PARA VISUALIZAR EL ALTA DEL PEDRIO
    path('catastro/perfil/registro_predios/',views.predios_index,name='vista_alta_predios'),

    #RUTA VISUALIZAR SOLICITUD DC017
    path('catastro/perfil/solicitud_dc017/',views.solicitud_dc017,name='solicitud'),

    #RUTA VISUALIZAR FICHA CATASTRAL
    path('catastro/perfil/ficha_catastral/',views.ficha_catastral,name='ficha_catastral'),
    
    #ENVIAR NOTIFICACION
    path('enviar/',views.enviar, name='not'),
    path('menu_willy',views.menu_willy, name='menu_w'),
    # Views POST
    path('registar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cambiar_contra/', views.cambiar_password, name='cambiar_password'),
    
    #PRUEBA_NOTIFY
    path('notify/',views.view_notify,name="view_notify"),
    path('send_not/',views.send_notify_test,name="send_not_2"),
    
]
