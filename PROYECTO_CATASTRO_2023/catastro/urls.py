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

    ############################ RUTAS QUE IMPLICA EL REGISTRO, MODIFICACION Y ELIMINACION DEL CONTRIBUYENTE #####

    #INICIO
    #página index de contribuyentes
    path('index_contribuyentes/',views.vista_index_contribuyente, name='index_contribuyente'),
    path('busqueda/',views.consulta_index_contribuyentes, name='busqueda_contribuyentes'),

    #CREATE
    #vista para visualzar pantalla de registro
    path('registro_contribuyente/',views.vista_alta_contribuyente,name='vista_alta_contribuyente'),
    # ruta para registrar al contribuyente
    path('registrar_contribuyente/',views.registro_contribuyente, name='registro_contribuyente'),

    #UPDATE
    #vista pantalla editar contribuyentes
    path('editar_contribuyente/<str:rfc>/',views.vista_update_contribuyentes, name='modificacion_contribuyentes'),
    #ruta que actualiza los datos del contribuyente
    path('update_contribuyente/<str:rfc_u>/',views.update_contribuyentes,name='update_contribuyentes'),

    #DELETE
    path('delete_contribuyente/<str:rfc_u>/',views.delete_contribuyentes,name='delete_contribuyentes'),
    ###################################


    ############################ RUTAS QUE IMPLICA EL REGISTRO, MODIFICACION Y ELIMINACION DE UN PREDIO #####

    #INICIO
    #vista para el inicio de predios
    path('index_predios/',views.vista_index_predios, name='index_predios'),
    path('busqueda_predios/',views.consulta_index_predios, name='busqueda_predios'),

    #CREATE
    #vista para visualzar pantalla de registro
    path('registro_predios/',views.vista_alta_predios,name='vista_alta_predios'),
    # ruta para registrar al predio
    path('registrar_predios/',views.registro_predios, name='registro_predios'),

    #UPDATE
    #vista pantalla editar contribuyentes
    #path('editar_predios/<str:clave>/',views.vista_update_predios, name='modificacion_predios'),
    #ruta que actualiza los datos del contribuyente
    #path('update_predios/<str:clave>/',views.update_predios,name='update_predios'),

    #DELETE
    #path('delete_contribuyente/<str:clave>/',views.delete_predios,name='delete_predios'),
    






    #RUTA VISUALIZAR SOLICITUD DC017
    path('catastro/perfil/solicitud_dc017/',views.solicitud_dc017,name='solicitud'),
    path('catastro/perfil/solicitud_dc017/registrar_solicitud',views.registrar_solicitud_dc017,name='registrar_solicitud'),


    #RUTA VISUALIZAR FICHA CATASTRAL
    path('catastro/perfil/ficha_catastral/',views.ficha_catastral,name='ficha_catastral'),
    path('catastro/perfil/ficha_catastral/redirigir',views.redirigir,name='redirect'),


    #RUTA PARA CONSULTAR DATOS GENERALES DE LA FICHA CATASTRAL
    path('catastro/perfil/ficha_catastral/ajax_ficha/',views.obtener_datos_busqueda_ficha),


    #RUTAS PARA REGISTRAR INFORMACIÓN DE LA FICHA CATASTRAL
    #TERRENOS RURALES
    path('catastro/perfil/ficha_catastral/registrar_ficha',views.registrar_ficha_datosgenerales,name='ficha'),
    path('catastro/perfil/ficha_catastral/registrar_datosrurales',views.registrar_ficha_terrenos_rurales,name='rural'),
    path('catastro/perfil/ficha_catastral/registrar_datosrurales_supertotal',views.registrar_ficha_terrenos_rurales_supertotal,name='rural_supertotal'),
    

    #TERRENOS URBANOS
    path('catastro/perfil/ficha_catastral/registrar_datosurbanos',views.registrar_ficha_terrenos_urbanos,name='urbano'),
    path('catastro/perfil/ficha_catastral/registrar_datosurbanos_incremento',views.registrar_ficha_terrenos_urbanos_incremento,name='urbano_incremento'),
    path('catastro/perfil/ficha_catastral/registrar_datosurbanos_demeritos',views.registrar_ficha_terrenos_urbanos_demeritos,name='urbano_demerito'),


    #DATOS CONSTRUCCION
    path('catastro/perfil/ficha_catastral/registrar_datosconstruccion',views.registrar_ficha_datos_construcciones,name='dconstruccion'),


    #ENVIAR NOTIFICACION
    path('enviar/',views.send_notify_test, name='not'),
    
    # Views POST
    path('registar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cambiar_contra/', views.cambiar_password, name='cambiar_password'),
    
    #PRUEBA_NOTIFY
    path('notify/',views.view_notify,name="view_notify"),
    path('send_not/',views.send_notify_test,name="send_not_2"),
    
]
