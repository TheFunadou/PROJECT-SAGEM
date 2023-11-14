
import datetime
from catastro import models as models_cat
from finanzas import models as models_fin
from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
import json
import os
from catastro import functions
from num2words import num2words
from report.report import report

def reporte_pago_predial(request,cajero, clave_cat, ejercicios, folio, observaciones):
    query_datos_grales_cont= models_cat.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    query_datos_pred = models_cat.Datos_gen_predio.objects.get(clave_catastral=clave_cat)
    contribuyente = models_cat.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    query_datos_pago = models_fin.pago_predial.objects.get(Q(contribuyente=contribuyente) & Q(estatus = 'PAGADO') & Q(folio = folio))
    fecha_hora_actual = datetime.datetime.now()
    
    impuesto_predial = "{:.2f}".format(query_datos_pago.impuesto_predial)
    impuesto_adicional = "{:.2f}".format(query_datos_pago.impuesto_adicional)
    multa = "{:.2f}".format(query_datos_pago.multa)
    recargo = "{:.2f}".format(query_datos_pago.recargo)
    descuento = "{:.2f}".format(query_datos_pago.descuento)
    total = "{:.2f}".format(query_datos_pago.total)
    
    str_total = str(total)
    parte_entera, parte_decimal = map(int, str_total.split('.'))
    str_parte_decimal = "00" if parte_decimal == 0 else parte_decimal
    
    data = {
        'cajero':cajero,
        'folio': folio,
        'fecha_hora':fecha_hora_actual.strftime("%d/%m/%Y %H:%M"),
        'propietario':f'{query_datos_grales_cont.nombre} {query_datos_grales_cont.apaterno} {query_datos_grales_cont.amaterno}',
        'domicilio':f'{query_datos_grales_cont.calle} #{query_datos_grales_cont.num_ext},{query_datos_grales_cont.colonia_fraccionamiento},{query_datos_grales_cont.codigo_postal}',
        'localidad': query_datos_grales_cont.localidad,
        'clave_cat': clave_cat,
        'tipo_predio':query_datos_pred.tipo_predio,
        'valor_catastral':'',
        'concepto': f'PAGO DE IMPUESTO PREDIAL {ejercicios}',
        'observaciones':observaciones,
        'impuesto_predial':f'$ {impuesto_predial}',
        'impuesto_adicional':f'$ {impuesto_adicional}',
        'multas':f'$ {multa}',
        'recargos':f'$ {recargo}',
        'descuento':f'($ {descuento})',
        'total': f'$ {total} M.N',
        'total_txt':f"({num2words(parte_entera,lang='es')} pesos {str_parte_decimal}/100 M.N)",
        'codigo_qr':'prueba'
    }
    
    return report(request, 'prueba', data)



# def reporte_pago_predial(cajero, clave_cat, ejercicios, folio, observaciones):
#     query_datos_grales_cont= models_cat.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
#     query_datos_pred = models_cat.Datos_gen_predio.objects.get(clave_catastral=clave_cat)
#     contribuyente = models_cat.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
#     query_datos_pago = models_fin.pago_predial.objects.get(Q(contribuyente=contribuyente) & Q(estatus = 'PAGADO') & Q(folio = folio))
    
#     fecha_hora_actual = datetime.datetime.now()
    
#     data = {'data': [{
        
#         'folio':query_datos_pago.folio,
#         'propietario':f'{query_datos_grales_cont.nombre} {query_datos_grales_cont.apaterno} {query_datos_grales_cont.amaterno}',
#         'domicilio':f'{query_datos_grales_cont.calle} #{query_datos_grales_cont.num_ext},{query_datos_grales_cont.colonia_fraccionamiento},{query_datos_grales_cont.codigo_postal}',
#         'localidad': query_datos_grales_cont.localidad,
#         'clave_cat': clave_cat,
#         'tipo_predio':query_datos_pred.tipo_predio,
#         # VALOR CATASTRAL SE OBTIENE AL GUARDAR REGISTROS DE LA FICHA CATASTRAL
#         'valor_catastral':'',
#         'impuesto_predial':f'{query_datos_pago.impuesto_predial}',
#         'impuesto_adicional':f'{query_datos_pago.impuesto_adicional}',
#         'multas':f'{query_datos_pago.multa}',
#         'recargos':f'{query_datos_pago.recargo}',
#         'concepto': f'PAGO DE IMPUESTO PREDIAL {ejercicios}',
#         'descuento':f'{query_datos_pago.descuento}',
#         'total':f'{query_datos_pago.total} MXN',
#         'observaciones':observaciones,
#         'cajero':cajero,
#         'fecha_hora':fecha_hora_actual.strftime("%d/%m/%Y %H:%M"),
#         'total_txt':f"{num2words(query_datos_pago.total,lang='es')} pesos"
#     }]}
    
#     # Crear archivo.json
#     crear_json = json.dumps(data)

#     ruta_relativa_json = 'finanzas/reports/PAGO_PREDIAL/PAGO_PREDIAL.json'
    
#     # Cargar scrpit al archivo.json
#     with open(ruta_relativa_json, "w", encoding="cp1250") as file:
#         file.write(crear_json)
#     file.close

#     # Ruta carpeta documentos en One Drive
#     ruta_carpeta = os.path.join(
#         os.path.expanduser("~"), "OneDrive", "Documentos")
#     ruta_carpeta = ruta_carpeta+'\REPORTES_CATASTRO\RECIBO_PAGO_PREDIAL'
#     ruta_carpeta = ruta_carpeta.replace('\\', '/')

#     # Buscar si existe una carpeta RECIBO_PAGO_PREDIAL de lo contrario crearla
#     if not os.path.exists(ruta_carpeta):
#         os.makedirs(ruta_carpeta)

#     ruta_relativa_jrxml = 'finanzas/reports/PAGO_PREDIAL/PAGO_IMPUESTO_PREDIAL.jrxml'

#     # Archivo de salida que se almacenara en la carpeta RECIBO_PAGO_PREDIAL
#     arch_sal = ruta_carpeta+'/PAGO_PREDIAL'+clave_cat

#     functions.crear_reporte(ruta_relativa_json,ruta_relativa_jrxml,arch_sal)
    
#     return HttpResponse ('Ok')

