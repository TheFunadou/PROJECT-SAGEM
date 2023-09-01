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
    path('redirigir_perf_fin/', views.redirigir_finanzas, name='redirigir_perfil_finanzas'),
    
    #GESTOR_NOTIFY
    path('gestor_notify_finanzas/',views.gestor_notify_finanzas, name= 'gestor_notify_finanzas'),

    #FINANZAS pago 1 (contribuyente al corriente)
    path('buscar_adeudo/',views.buscar_adeudos, name='buscar_adeudos'),
    path('buscar_adeudo/ajax/',views.obtener_datos_busqueda, name='buscar'),
    path('buscar_adeudo/ajax/<str:dato>/',views.busqueda_valida_adeudos, name='validar_adeudos'),
    path('buscar_adeudo/ajax/<str:dato>/redireccionar/',views.redireccionar_menu, name='redireccionar'),
    
    path('buscar_adeudo/ajax/<str:dato>/solicitar',views.solicitar_descuento),
    ####################

    #path('redireccionar/',views.redireccionar_menu_su, name='redireccionar_su'),
    
   

   #PANTALLAS DE SELECCION DE CONTRIBUYENTES CON DESCUENTOS Y POR APLICAR
    #path('descuento_aplicado/',views.pantalla_seleccion_cajera, name='descuento_aplicado'),
    path('menu_principal/menu_finanzas/descuento_pendiente/',views.pantalla_seleccion_contadora, name='descuento_pendiente'),


    path('menu_principal/menu_finanzas/descuento_aprobado/',views.pantalla_seleccion_cajera, name='descuento_aprobado'),

    path('perfil_su/xd/',views.notificaciones_contabilizar),
    path('perfil/cajera/',views.notificaciones_contabilizar_cajera),
    #RUTAS PARA PANTALLA APLICAR DESCUENTO
    path('descuento_pendiente/aplicar_descuento/<str:dato>',views.aplicar_descuentos, name='aplicar_descuento'),
    path('descuento_aplicado/<str:dato>',views.redireccionar_menu_su, name='descuento_aplicado'),
   
    
    
]
