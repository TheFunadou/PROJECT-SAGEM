from catastro import models as models_catastro
from catastro import functions
import os
from pyreportjasper import PyReportJasper
import json
import datetime
import webbrowser



def REPORTE_TEST():
    # Crear scrpit json
    
    print("REPORTE TEST PRUEBA 1")
    lista=[]
    
    query = models_catastro.Datos_gen_predio.objects.values_list('clave_catastral', flat=True)
    
    # print(query)
    
    for rs in query:
        lista.append(rs)
    
    print(lista)
    
    data = {'data': [{
        # DATOS USUARIO
        'NOM_USER':lista,
        
    }]}
    
    # Crear archivo.json
    crear_json = json.dumps(data)

    ruta_arch_json = 'catastro/static/reports/TEST/TEST.json'

    # Cargar scrpit al archivo.json
    with open(ruta_arch_json, "w", encoding="cp1250") as file:
        file.write(crear_json)
    file.close

    # Ruta carpeta documentos en One Drive
    ruta_carpeta = os.path.join(
        os.path.expanduser("~"), "OneDrive", "Documentos")
    ruta_carpeta = ruta_carpeta+'\REPORTES_CATASTRO\DC017'
    ruta_carpeta = ruta_carpeta.replace('\\', '/')

    # Buscar si existe una carpeta REPORTES_CATASTRO de lo contrario crearla
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    # Archivo de entrada jrxml
    ruta_arch_dc017='catastro/static/reports/TEST/TEST_REPORTE.jrxml'

    # Archivo de salida que se almacenara en la carpeta REPORTES_CATASTRO
    arch_sal = ruta_carpeta+'/TEST'

    # functions.crear_reporte(ruta_arch_json,ruta_arch_dc017,arch_sal)
    
# Conexion con la hoja json
    conn = {
        'driver': 'json',
        'data_file': ruta_arch_json,
        'json_query': 'data'
    }

    # Crear el reporte con PyReportJasper
    pyreportjasper = PyReportJasper()
    # Configuracion del reporte
    pyreportjasper.config(
        input_file=ruta_arch_dc017,
        output_file=arch_sal,
        output_formats=['pdf'],
        locale='es_MX',
        db_connection=conn)

    # Creacion del reporte
    pyreportjasper.process_report()

    # Abrir el archivo en el navegador
    webbrowser.open_new_tab(arch_sal+'.pdf')

