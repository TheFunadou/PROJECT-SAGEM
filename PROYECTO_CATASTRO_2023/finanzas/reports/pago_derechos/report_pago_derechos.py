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

def report_pago_derecho(request,folio,clave_cat):
    query = models_fin.detalle_pago_derecho.objects.select_related('id_pago','id_derecho').get(id_pago__folio=folio)
    datos_contrib = models_cat.Datos_Contribuyentes.objects.get(clave_catastral = clave_cat)
    
    fecha_hora_actual = datetime.datetime.now()
    subtotal = "{:,.2f}".format(float(query.id_pago.subtotal))
    descuento = "{:,.2f}".format(float(query.id_pago.descuento))
    impuesto_adicional = "{:,.2f}".format(float(query.id_pago.impuesto_adicional))
    total = "{:,.2f}".format(float(query.id_pago.total))
    
    parts = total.replace(',','').split('.')
    str_part_decimal = '00' if parts[1] == '0' else parts[1]
    
    first_letter = str(num2words(parts[0],lang='es'))[0].upper()
    last_word = str(num2words(parts[0],lang='es'))[1:]
    num_to_word = first_letter+last_word
    
    
    data = {
        'cajero':request.user.username,
        'folio': folio,
        'fecha_hora':fecha_hora_actual.strftime("%d/%m/%Y %H:%M"),
        'contribuyente':f'{datos_contrib.nombre} {datos_contrib.apaterno} {datos_contrib.amaterno}',
        'concepto': f'{query.concepto}',
        'observaciones':query.observaciones,
        'cantidad':'1',
        'subtotal':f'${subtotal}',
        'descuento':f'${descuento}',
        'total':f'${total} M.N',
        'impuesto_adicional':f'{impuesto_adicional}',
        'total_txt':f"({num_to_word} pesos {str_part_decimal}/100 M.N.)",
        'codigo_qr':'prueba'
    }
    
    return report(request, 'report_pago_derecho', data)