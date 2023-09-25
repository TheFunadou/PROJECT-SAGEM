
from catastro import models as models_cat
from finanzas import models as models_fin
from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
import json
import os
from catastro import functions

def reporte_pago_predial_ad(cajero, clave_cat, ejercicios, observaciones):
    
    
    query_datos_grales_cont= models_cat.Datos_Contribuyentes.objects.filter(clave_catastral=clave_cat)
    
    for qdc in query_datos_grales_cont:
        nombre_completo = f'{qdc.nombre} {qdc.apaterno} {qdc.amaterno}'
        domicilio = f'{qdc.calle} #{qdc.num_ext},{qdc.colonia_fraccionamiento}'
        localidad = qdc.localidad
        
    query_datos_pred = models_cat.Datos_gen_predio.objects.filter(clave_catastral=clave_cat)
    
    for qdp in query_datos_pred:
        tipo_predio = qdp.tipo_predio
        # valor_cat
    
    contribuyente = models_cat.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    
    query_datos_pago = models_fin.historial_pagos.objects.filter(contribuyente_id=contribuyente)
    
    for qdp in query_datos_pago:
        folio = qdp.folio
        impuesto_adicional = qdp.impuesto_adicional
        recargos= qdp.recargo
        multas = qdp.multa
        total = qdp.total
    
    
    data = {'data': [{
        
        'folio':folio,
        'propietario':nombre_completo,
        'domicilio':domicilio,
        'localidad': localidad,
        'clave_cat': clave_cat,
        'tipo_predio':tipo_predio,
        'valor_catastral':'$ 2400000 MXN',
        'impuesto_adicional':f'{impuesto_adicional} MXN',
        'impuesto_predial':'',
        'multas':f'{multas} MXN',
        'recargos':f'{recargos} MXN',
        'honorarios':f'0 MXN',
        'concepto': f'PAGO PREDIAL AÑOS {ejercicios}',
        'descuento':f'{multas+recargos} MXN',
        'total':f'{total} MXN',
        'observaciones':observaciones,
        'cajero':cajero,
    }]}
    
    # Crear archivo.json
    crear_json = json.dumps(data)

    # Establecer ruta y nombre de archivo.json
    arch_json='reporte_pago_predial_ad.json'
    ruta_json = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_json = os.path.join(ruta_json, 'jrxml', arch_json)
    
    # Cargar scrpit al archivo.json
    with open(ruta_archivo_json, "w", encoding="cp1250") as file:
        file.write(crear_json)
    file.close

    # Ruta carpeta documentos en One Drive
    ruta_carpeta = os.path.join(
        os.path.expanduser("~"), "OneDrive", "Documentos")
    ruta_carpeta = ruta_carpeta+'\REPORTES_CATASTRO\RECIBO_PAGO_PREDIAL'
    ruta_carpeta = ruta_carpeta.replace('\\', '/')

    # Buscar si existe una carpeta REPORTES_CATASTRO de lo contrario crearla
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    # Archivo de entrada jrxml
    arch_jrxml='RECIBO_PAGO_AD.jrxml'
    ruta_jrxml = os.path.dirname(os.path.abspath(__file__))
    arch_ent = os.path.join(ruta_jrxml,'jrxml', arch_jrxml)

    # Archivo de salida que se almacenara en la carpeta REPORTES_CATASTRO
    arch_sal = ruta_carpeta+'/PAGO_PREDIAL'+clave_cat

    functions.crear_reporte(ruta_archivo_json,arch_ent,arch_sal)
    
    return HttpResponse ('Ok')