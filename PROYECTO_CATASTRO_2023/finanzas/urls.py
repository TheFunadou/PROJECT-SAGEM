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
from finanzas import views

app_name='finanzas'

#FINANZAS URLS
urlpatterns = [
    #CERRAR_SESION
    path('logout_finanzas/', views.cerrar_sesion, name='logout_finanzas'),
    #PERFIL USUARIO NORMAL
    path('perfil/',views.perfil_finanzas,name='perfil_fin'),
    #PERFIL SUPER USUARIO
    path('perfil_su/',views.perfil_sup_user_finanzas,name='perfil_su_fin'),
    
    
]
