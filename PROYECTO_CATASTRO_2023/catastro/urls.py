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
    path('perfil/',views.perfil_catastro,name='perfil_cat'),
    #PERFIL SUPER USUARIO
    path('perfil_su/',views.perfil_sup_user_catastro,name='perfil_su_cat'),
    
    path('perfil_su/prueba/',views.vista_prueba,name='prueba_notify'),
    
    # REGISTRAR NUEVOS CONTIBUYENTES
    #path('registro_contribuyente/',views.registrar_contribuyentes.as_view(), name='registro_contribuyente'),
    
    #ENVIAR NOTIFICACION
    path('enviar/',views.enviar, name='not'),
    path('menu_willy',views.menu_willy, name='menu_w')
    
    
]
