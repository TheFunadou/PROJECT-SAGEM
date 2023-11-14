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
from django.urls import include,path
from . import views_proyecto
#reporrbro
from report.views import Index
from report.report import *
#RUTAS GLOBALES


urlpatterns = [
    path('admin/', admin.site.urls),
    path('make_report/', Index.as_view(), name='index'),
    # REGISTRO DE USUARIO BETA
    # path('',views_proyecto.registrar_usuarios, name='registro_user'),
    
    #INICIO DE SESION
    path('',views_proyecto.pagina_login, name="pag_login"),
    path('login/',views_proyecto.autenticacion,name="autenticacion"),
    
    #Cerrar sesion
    path('logout/', views_proyecto.cerrar_sesion, name='logout'),
    
    #IMPORTAR APLICACIONES
    path('catastro/',include('catastro.urls', namespace='catastro')),
    path('finanzas/',include('finanzas.urls', namespace='finanzas')),
    path('desarrollo_urbano/',include('desarrollo_urbano.urls',namespace='desarrollo_urbano')),
    path('report/', include(('report.urls', 'report'))),
    

    #IMPORTAR FUNCIONALIDADES DE REPORTES
    path('edit/<str:report_type>/', edit , name='report_edit'),
    path('run/', run , name='report_run'),
    path('save/<str:report_type>/', save , name='report_save'),
    
]
