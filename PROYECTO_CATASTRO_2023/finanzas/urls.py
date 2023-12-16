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
# from .reports.reporte_pago_predial import reporte_pago_predial, reporte_pago_predial_2
from finanzas.reports.reporte_pago_predial import reporte_pago_predial
from finanzas.reports.pago_derechos.report_pago_derechos import report_pago_derecho

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
    
    path('pago_predial/solicitar_descuento',views.solicitar_descuento, name="solicitar_descuento"),
    ####################
    
   #PANTALLAS DE SELECCION DE CONTRIBUYENTES CON DESCUENTOS Y POR APLICAR
    path('descuento_aplicado/',views.pantalla_seleccion_cajera, name='descuento_aplicado'),
    path('menu_principal/menu_finanzas/descuento_pendiente/',views.view_seleccion_descuentos_solicitados, name='seleccion_descuentos_pendientes'),
    path('menu_principal/menu_finanzas/descuento_aprobado/',views.view_seleccion_descuentos_aprobados, name='seleccion_descuentos_aprobados'),
    #RUTAS PARA PANTALLA APLICAR DESCUENTO
    path('descuento_pendiente/aplicar_descuento/<str:dato>/',views.aplicar_descuentos, name='aplicar_descuento'),
    # PAGO PREDIAL
    path('pago_predial/descuento_aprobado/<str:dato>/',views.view_pago_descuento_aprobado, name='pago_descuento_aprobado'),
    path('aprobar_descuento_contribuyente/',views.descuento_aprobado, name='aprobar_descuento'),
    path('rechazar_descuento_contribuyente/',views.descuento_rechazado, name='rechazar_descuento'),
    path('pago_predial_contribuyente_years_debe_directo/',views.pago_predial, name='pago_predial'),

    
    #VISTAS REPORTES
    path('reporte_pago_predial/<str:cajero>/<str:clave_cat>/<str:ejercicios>/<str:folio>/<str:observaciones>/', reporte_pago_predial, name='reporte_pago_predial'),
    
    #----------------PAGO DE DERECHOS----------------
    path('pago_derechos/',views.view_pago_derechos, name='view_pago_derecho'),
    path('search_derechos/',views.search_derechos, name='search_derechos'),
    path('search_precio_derecho/',views.search_precio_derecho, name='search_precio_derecho'),
    path('pago_derecho/',views.pago_derecho, name='pago_derecho'),
    path('reporte_pago_derecho/<str:cajero>/<str:nombre>/<str:observaciones>/<str:concepto>/<str:cantidad>/<str:subtotal>/<str:descuento>/<str:impuesto_adicional>/<str:total>/', report_pago_derecho, name='reporte_pago_derecho'),
]

