from catastro import models
from catastro import functions
from django.db.models import Case, When, Value, CharField
import datetime

def crear_ficha_catastral(data,clave_cat,cajero,titular_cat):

# DATOS DEL CONTRIBUYENTE
    query_datos_c = models.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
# DATOS DIRECCION INMUEBLE
    query_domicilio_inm = models.Domicilio_inmueble.objects.get(pk_fk_clave_catastral_id=clave_cat)
# DATOS USO O DESTINO DEL PREDIO
    query_datos_inm = models.Datos_inmuebles.objects.get(fk_clave_catastral_id=clave_cat)
# DOMICILIO NOTIFICACIONES
    query_dom_notify = models.Domicilio_noti.objects.get(fk_rfc_id = query_datos_c)
# DATOS DOCUMENTO PREDIO
    query_doc_pred= models.datos_documento_predio.objects.get(pk_clave_catastral=clave_cat)
# DATOS PREDIO
    query_datos_predio= models.datos_predio_ficha.objects.get(pk_clave_catastral=clave_cat)
# DATOS INSCRIPCION
    query_datos_insc_actual= models.datos_inscripcion.objects.get(pk_fk_clave_catastral=clave_cat,tipo='ACTUAL')
    query_datos_insc_antecedente= models.datos_inscripcion.objects.get(pk_fk_clave_catastral=clave_cat,tipo='ANTECEDENTE')
# DATOS TERRENOS RURALES ################
    query_datos_tr = models.terrenos_rurales.objects.filter(pk_fk_clave_catastral=clave_cat)
    
    datos_tr = {
        "TIP_SUE_TR_1":'',
        "VAL_HAS_TR_1":'',
        "HAS_TR_1":'',
        "A_TR_1":'',
        "C_TR_1":'',
        "TOP_TR":'',
        "VIAS_TR":'',
        "TIP_SUE_TR_2":'',
        "VAL_HAS_TR_2":'',
        "HAS_TR_2":'',
        "A_TR_2":'',
        "C_TR_2":'',
        "TIP_SUE_TR_3":'',
        "VAL_HAS_TR_3":'',
        "HAS_TR_3":'',
        "A_TR_3":'',
        "C_TR_3":'',
        "TIP_SUE_TR_4":'',
        "VAL_HAS_TR_4":'',
        "HAS_TR_4":'',
        "A_TR_4":'',
        "C_TR_4":''
    }
    
    cont = 1
    
    for rs in query_datos_tr:
        datos_tr[f'TIP_SUE_TR_{cont}']= rs.tipo_suelo
        datos_tr[f'VAL_HAS_TR_{cont}']= rs.valor_has
        datos_tr[f'HAS_TR_{cont}']= rs.sup_has
        datos_tr[f'A_TR_{cont}']= rs.a
        datos_tr[f'C_TR_{cont}']= rs.c
        datos_tr['TOP_TR']= rs.top
        datos_tr['VIAS_TR']= rs.vias_c 
        cont = cont+1 
             
    query_datos_tr_sup_total = models.terrenos_rurales_superficietotal.objects.get(pk_fk_clave_catastral=clave_cat)
   
# DATOS TERRENOS URBANOS Y SUBURBANOS

    query_datos_us = models.terrenos_urbanos_suburbanos.objects.filter(fk_clave_catastral=clave_cat)
    
    datos_us={
        "VAL_M2_DUS":'',
        "ARE_TER_DUS":'',
        "T_C_DUS_1":'',
        "T_VAL_M2_DUS_1":'',
        "T_FRE_DUS_1":'',
        "T_PROF_DUS_1":'',
        "T_C_DUS_2":'',
        "T_VAL_M2_DUS_2":'',
        "T_FRE_DUS_2":'',
        "T_PROF_DUS_2":'',    
        "T_C_DUS_3":'',
        "T_VAL_M2_DUS_3":'',
        "T_FRE_DUS_3":'',
        "T_PROF_DUS_3":'',
        "T_C_DUS_4":'',
        "T_VAL_M2_DUS_4":'',
        "T_FRE_DUS_4":'',
        "T_PROF_DUS_4":''
    }
    
    cont2=1

    for rs in query_datos_us:
        datos_us['VAL_M2_DUS']= rs.valor_m2
        datos_us['ARE_TER_DUS']= rs.area
        datos_us[f'T_C_DUS_{cont2}']= rs.c
        datos_us[f'T_VAL_M2_DUS_{cont2}']= rs.valor
        datos_us[f'T_FRE_DUS_{cont2}']= rs.frente
        datos_us[f'T_PROF_DUS_{cont2}']= rs.profundidad
        cont2 = cont2+1 
    
    # DEMERITOS PREDIOS URBANOS
    query_datos_us_demeritos = models.demeritos_predios_urbanos.objects.filter(fk_clave_catastral = clave_cat)
    
    orden_demeritos_const = Case(
        When(estado="Interés Social", then=Value(0)),
        When(estado="Excedente de área", then=Value(1)),
        When(estado="Topografía", then=Value(2)),
        When(estado="Cond. Física imprevista", then=Value(3)),
        default=Value(4),  # Si hay valores que no están en la lista, se colocarán al final
        output_field=CharField(),
    )
    
    query_datos_us_demeritos = query_datos_us_demeritos.annotate(orden_demeritos_const).order_by('descripcion')
    
    lista_demeritos_datos_const= []
    
    for rs in query_datos_us_demeritos:
        lista_demeritos_datos_const.append(rs.valor)
    
    
    # INCREMENTO POR ESQUINA
    query_datos_us_incremento_esq = models.incrementos_esquina_urbanos.objects.filter(fk_clave_catastral=clave_cat)
    
    orden_demeritos_incremento_esq = Case(
        When(estado="A", then=Value(0)),
        When(estado="B", then=Value(1)),
        When(estado="C", then=Value(2)),
        When(estado="D", then=Value(3)),
        default=Value(4),  # Si hay valores que no están en la lista, se colocarán al final
        output_field=CharField(),
    )
    
    query_datos_us_incremento_esq = query_datos_us_incremento_esq.annotate(orden_demeritos_incremento_esq).order_by('tipo')

    lista_demeritos_incremento_esq = []
    
    for rs in query_datos_us_incremento_esq:
        lista_demeritos_incremento_esq.append(rs.valor)

    # DATOS CONSTRUCCIONES

    query_datos_cons = models.ficha_datos_construcciones.objects.filter(fk_clave_catastral=clave_cat)
    
    datos_const={
        "DAT_C_TIPO_1":'',
        "DAT_C_EDO_1":'',
        "DAT_C_T_1":'',
        "DAT_C_ANT_1":'',
        "DAT_C_ARE_M2_1":'',
        "DAT_C_TIPO_2":'',
        "DAT_C_EDO_2":'',
        "DAT_C_T_2":'',
        "DAT_C_ANT_2":'',
        "DAT_C_ARE_M2_2":'',
        "DAT_C_TIPO_3":'',
        "DAT_C_EDO_3":'',
        "DAT_C_T_3":'',
        "DAT_C_ANT_3":'',
        "DAT_C_ARE_M2_3":'',
        "DAT_C_TIPO_4":'',
        "DAT_C_EDO_4":'',
        "DAT_C_T_4":'',
        "DAT_C_ANT_4":'',
        "DAT_C_ARE_M2_4":'',
        "DAT_C_TIPO_5":'',
        "DAT_C_EDO_5":'',
        "DAT_C_T_5":'',
        "DAT_C_ANT_5":'',
        "DAT_C_ARE_M2_5":''
    }
    
    cont3=1

    for rs in query_datos_cons:
        datos_const[f'DAT_C_TIPO_{cont3}']= rs.tipo_c
        datos_const[f'DAT_C_EDO_{cont3}']= rs.est
        datos_const[f'DAT_C_T_{cont3}']= rs.terreno
        datos_const[f'DAT_C_ANT_{cont3}']= rs.antiguedad
        datos_const[f'DAT_C_ARE_M2_{cont3}']= rs.area_c
        cont3 = cont3+1 

    # VALORES
    query_datos_valores_cat = models.valores_catastro.objects.get(clave_catastral_pk=clave_cat)

    #functions.reporte_ficha_cat(datos_clav_c,datos_gral,datos_doc,datos_pred,datos_rp,datos_tr,datos_us,datos_const)

    # OBTENER FECHA
    fecha_hora_actual = datetime.datetime.now()
    datos = {'datos': [{
        # DAT_DOC
        'TP_MOV':'',
        'TIP_PRED':'',
        'FOLIO':data.folio,
        'FECHA':fecha_hora_actual.strftime("%d/%m/%Y %H:%M"),
        # CLAVE CATASTRAL
        
        # DATOS CONTRIBUYENTE
        'NOM_GRAL': query_datos_c.nombre,
        'AP_GRAL': query_datos_c.apaterno,
        'AM_GRAL': query_datos_c.amaterno,
        'RFC_GRAL': query_datos_c.rfc,

        # UBIACION DEL PREDIO
        'CALL_INM_GRAL': query_domicilio_inm.calle,
        'NUM_EXT': query_domicilio_inm.num_ext,
        'NUM_INT': query_domicilio_inm.num_int,
        'COL_FRA_GRAL':query_domicilio_inm.col_fracc,

        # USO O DESTINO DEL PREDIO
        'USO_DES_GRAL': query_datos_inm.uso_predio,

        #DOMICILIO PARA RECIBIR NOTIFICACIONES
        'CALLE_N': query_dom_notify.calle,
        'NUM_EXT_N': query_dom_notify.num_ext,
        'NUM_INT_N': query_dom_notify.num_int,
        # argregar columna codigo postal
        'COD_POS_N': '',
        'COL_O_FRA_INM_N': query_dom_notify.col,
        'CIUDAD_N': query_dom_notify.localidad,

        #DATOS DEL DOCUMENTO DE PROPIEDAD O POSESION
        'LUG_EXP_DOC':query_doc_pred.lugar_expedision,
        'TD_DOC': query_doc_pred.td,
        'NUM_DOC':query_doc_pred.num_documento,
        'DIA_DOC': query_doc_pred.dia,
        'MES_DOC':query_doc_pred.mes,
        'YEAR_DOC': query_doc_pred.año,
        'NOT_DOC':query_doc_pred.num_notaria,

        #DATOS DEL PREDIO
        'TIP_AVA_DP':query_datos_predio.tipo_avaluo,
        'FRAC_DP':query_datos_predio.fraccionamiento,
        'TRAS_DOM_DP':query_datos_predio.traslado_dominio,
        'REG_LEG_DP':query_datos_predio.regimen,
        'TEN_DP':query_datos_predio.tenencia,
        'EST_FIS_DP':query_datos_predio.estado_fisico,
        'COD_USO_DP':query_datos_predio.codigo_uso,
        'TIP_POS_DP':query_datos_predio.tipo_posecion,
        'NO_EMI_DP':query_datos_predio.num_emision,

        #DATOS DE INSCRIPCION EN EL REGISTRO PUBLICO DE LA PROPIEDAD
        'BN_ACT_DRP':query_datos_insc_actual.bajo_numero,
        'BN_ANTE_DRP':query_datos_insc_antecedente.bajo_numero,
        'TO_ACT_DRP':query_datos_insc_actual.tomo,
        'TO_ANTE_DRP':query_datos_insc_antecedente.tomo,
        'DIA_ACT_DRP':query_datos_insc_actual.dia_i,
        'DIA_ANTE_DRP':query_datos_insc_antecedente.dia_i,
        'MES_ACT_DRP':query_datos_insc_actual.mes_i,
        'MES_ANTE_DRP':query_datos_insc_antecedente.mes_i,
        'YEAR_ACT_DRP':query_datos_insc_actual.año_i,
        'YEAR_ANTE_DRP':query_datos_insc_antecedente.año_i,
        'ZON_ACT_DRP':query_datos_insc_actual.zona_i,
        'ZON_ANTE_DRP':query_datos_insc_antecedente.zona_i,

        #DATOS TERRENOS RURALES
        'TIP_SUE_TR_1':datos_tr['TIP_SUE_TR_1'],
        'VAL_HAS_TR_1':datos_tr['VAL_HAS_TR_1'],
        'HAS_TR_1':datos_tr['HAS_TR_1'],
        'A_TR_1':datos_tr['A_TR_1'],
        'C_TR_1':datos_tr['C_TR_1'],

        'TIP_SUE_TR_2':datos_tr['TIP_SUE_TR_2'],
        'VAL_HAS_TR_2':datos_tr['VAL_HAS_TR_2'],
        'HAS_TR_2':datos_tr['HAS_TR_2'],
        'A_TR_2':datos_tr['A_TR_2'],
        'C_TR_2':datos_tr['C_TR_2'],

        'TIP_SUE_TR_3':datos_tr['TIP_SUE_TR_3'],
        'VAL_HAS_TR_3':datos_tr['VAL_HAS_TR_3'],
        'HAS_TR_3':datos_tr['HAS_TR_3'],
        'A_TR_3':datos_tr['A_TR_3'],
        'C_TR_3':datos_tr['C_TR_3'],

        'TIP_SUE_TR_4':datos_tr['TIP_SUE_TR_4'],
        'VAL_HAS_TR_4':datos_tr['VAL_HAS_TR_4'],
        'HAS_TR_4':datos_tr['HAS_TR_4'],
        'A_TR_4':datos_tr['A_TR_4'],
        'C_TR_4':datos_tr['C_TR_4'],

        'TOP_TR':datos_tr['TOP_TR'],
        'VIAS_TR':datos_tr['VIAS_TR'],

        'INF_HAS_TR':'',
        'INF_A_TR':'',
        'INF_C_TR':'',

        'SUP_AG_HAS_TR':'',
        'SUP_AG_A_TR':'',
        'SUP_AG_C_TR':'',

        'SUP_T_HAS_TR':query_datos_tr_sup_total.sup_t_has,
        'SUP_T_A_TR':query_datos_tr_sup_total.a,
        'SUP_T_C_TR':query_datos_tr_sup_total.c,

        # DATOS TERRENOS URBANOS Y SUBURBANOS
        'VAL_M2_DUS':datos_us['VAL_M2_DUS'],
        'ARE_TER_DUS':datos_us['ARE_TER_DUS'],
        
        'T_C_DUS_1':datos_us['T_C_DUS_1'],
        'T_VAL_M2_DUS_1':datos_us['T_VAL_M2_DUS_1'],
        'T_FRE_DUS_1':datos_us['T_FRE_DUS_1'],
        'T_PROF_DUS_1':datos_us['T_PROF_DUS_1'],

        'T_C_DUS_2':datos_us['T_C_DUS_2'],
        'T_VAL_M2_DUS_2':datos_us['T_VAL_M2_DUS_2'],
        'T_FRE_DUS_2':datos_us['T_FRE_DUS_2'],
        'T_PROF_DUS_2':datos_us['T_PROF_DUS_2'],

        'T_C_DUS_3':datos_us['T_C_DUS_3'],
        'T_VAL_M2_DUS_3':datos_us['T_VAL_M2_DUS_3'],
        'T_FRE_DUS_3':datos_us['T_FRE_DUS_3'],
        'T_PROF_DUS_3':datos_us['T_PROF_DUS_3'],

        'T_C_DUS_4':datos_us['T_C_DUS_4'],
        'T_VAL_M2_DUS_4':datos_us['T_VAL_M2_DUS_4'],
        'T_FRE_DUS_4':datos_us['T_FRE_DUS_4'],
        'T_PROF_DUS_4':datos_us['T_PROF_DUS_4'],

        'INC_X_ESQ_DUS_A':lista_demeritos_incremento_esq[0],
        'INC_X_ESQ_DUS_B':lista_demeritos_incremento_esq[1],
        'INC_X_ESQ_DUS_C':lista_demeritos_incremento_esq[2],
        'INC_X_ESQ_DUS_D':lista_demeritos_incremento_esq[3],

        'DEM_INT_SOC_DUS':lista_demeritos_datos_const[0],
        'DEM_EXC_ARE_DUS':lista_demeritos_datos_const[1],
        'DEM_TOPO_DUS':lista_demeritos_datos_const[2],
        'DEM_COND_FIS_DUS':lista_demeritos_datos_const[3],

        # DATOS CONSTRUCCIONES

        'DAT_C_TIPO_A':datos_const['DAT_C_TIPO_1'],
        'DAT_C_EDO_A':datos_const['DAT_C_EDO_1'],
        'DAT_C_T_A':datos_const['DAT_C_T_1'],
        'DAT_C_ANT_A':datos_const['DAT_C_ANT_1'],
        'DAT_C_ARE_M2_A':datos_const['DAT_C_ARE_M2_1'],

        'DAT_C_TIPO_B':datos_const['DAT_C_TIPO_2'],
        'DAT_C_EDO_B':datos_const['DAT_C_EDO_2'],
        'DAT_C_T_B':datos_const['DAT_C_T_2'],
        'DAT_C_ANT_B':datos_const['DAT_C_ANT_2'],
        'DAT_C_ARE_M2_B':datos_const['DAT_C_ARE_M2_2'],

        'DAT_C_TIPO_C':datos_const['DAT_C_TIPO_3'],
        'DAT_C_EDO_C':datos_const['DAT_C_EDO_3'],
        'DAT_C_T_C':datos_const['DAT_C_T_3'],
        'DAT_C_ANT_C':datos_const['DAT_C_ANT_3'],
        'DAT_C_ARE_M2_C':datos_const['DAT_C_ARE_M2_3'],

        'DAT_C_TIPO_D':datos_const['DAT_C_TIPO_4'],
        'DAT_C_EDO_D':datos_const['DAT_C_EDO_4'],
        'DAT_C_T_D':datos_const['DAT_C_T_4'],
        'DAT_C_ANT_D':datos_const['DAT_C_ANT_4'],
        'DAT_C_ARE_M2_D':datos_const['DAT_C_ARE_M2_4'],

        'DAT_C_TIPO_E':datos_const['DAT_C_TIPO_5'],
        'DAT_C_EDO_E':datos_const['DAT_C_EDO_5'],
        'DAT_C_T_E':datos_const['DAT_C_T_5'],
        'DAT_C_ANT_E':datos_const['DAT_C_ANT_5'],
        'DAT_C_ARE_M2_E':datos_const['DAT_C_ARE_M2_5'],

        'DAT_C_V_TER':query_datos_valores_cat.valor_terreno,
        'DAT_C_VAL_CON':query_datos_valores_cat.valor_construccion,
        'DAT_C_VAL_CAT':query_datos_valores_cat.valor_catastral,
        
        'ELABORO':cajero,
        'TITULAR_CAT':titular_cat
    }]}