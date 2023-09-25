from catastro import models
from catastro import functions

def crear_ficha_catastral(datos_clav_c):

# DATOS DEL CONTRIBUYENTE
    query_datos_c = models.Datos_Contribuyentes.objects.filter(clave_catastral=datos_clav_c)

    for datos_p in query_datos_c:
        rfc = datos_p.rfc
        nombre = datos_p.nombre
        ap = datos_p.apaterno
        am = datos_p.amaterno
        calle = datos_p.calle
        num_int_c = datos_p. num_int
        num_ext_c = datos_p.num_ext
        col_fracc_c= datos_p.colonia_fraccionamiento
        codigo_postal = datos_p.codigo_postal

    num_ofi_con = functions.num_oficial(num_int_c,num_ext_c)

    datos_gral = {
        "RFC_GRAL": rfc,
        "NOM_GRAL": nombre,
        "AP_GRAL": ap,
        "AM_GRAL": am,
        "CALLE_N": calle,
        "NUM_O_INM_N":num_ofi_con ,
        "COL_O_FRA_INM_N": col_fracc_c,
        "COD_POS_N": codigo_postal
    }

# DATOS DIRECCION INMUEBLE
    query_direccion_inm = models.Domicilio_inmueble.objects.filter(pk_fk_clave_catastral=datos_clav_c)

    for dom_inm in query_direccion_inm:
        calle = dom_inm.calle
        col_fracc_inm=dom_inm.col_fracc
        num_int_inm = dom_inm.num_int
        num_ext_inm = dom_inm.num_ext

    num_ofi_inm=functions.num_oficial(num_int_inm,num_ext_inm)

    datos_inm = {
        "CALL_INM_GRAL": calle,
        "COL_FRA_GRAL": col_fracc_inm,
        "NUM_O_GRAL": num_ofi_inm
    }

    datos_gral.update(datos_inm)

# DATOS USO O DESTINO DEL PREDIO
    query_datos_inm = models.Datos_inmuebles.objects.filter(fk_clave_catastral=datos_clav_c)

    for d_inm in query_datos_inm:
        uso_d = d_inm.uso_predio

    detalles_inm = {
        "USO_DES_GRAL": uso_d
    }

    datos_gral.update(detalles_inm)

# DATOS DOCUMENTO PREDIO
    query_doc_pred= models.datos_documento_predio.objects.filter(pk_clave_catastral=datos_clav_c)

    for doc_pred in query_doc_pred:
        lugar_exp= doc_pred.lugar_expedision
        td = doc_pred.td
        num_doc = doc_pred.num_documento
        dia = doc_pred.dia
        mes = doc_pred.mes
        year = doc_pred.año
        not_no = doc_pred.num_notaria

    datos_doc = {
        "LUG_EXP_DOC": lugar_exp,
        "TD_DOC": td,
        "NUM_DOC": num_doc ,
        "DIA_DOC": dia ,
        "MES_DOC": mes ,
        "YEAR_DOC":year ,
        "NOT_DOC": not_no
    }
    

# DATOS PREDIO
    query_datos_predio= models.datos_predio_ficha.objects.filter(pk_clave_catastral=datos_clav_c)

    for dat_pred in query_datos_predio:
        tipo_ava= dat_pred.tipo_avaluo
        fracc = dat_pred.fraccionamiento
        tras_dom = dat_pred.traslado_dominio
        regi = dat_pred.regimen
        tenen = dat_pred.tenencia
        est_fis = dat_pred.estado_fisico
        cod_uso = dat_pred.codigo_uso
        tipo_pos = dat_pred.tipo_posecion
        num_emi = dat_pred.num_emision
        uso_pred = dat_pred.uso_predio

    datos_pred = {
        "TIP_AVA_DP": tipo_ava,
        "FRAC_DP": fracc,
        "TRAS_DOM_DP": tras_dom ,
        "REG_LEG_DP": regi ,
        "TEN_DP": tenen ,
        "EST_FIS_DP":est_fis ,
        "COD_USO_DP": cod_uso,
        "TIP_POS_DP":tipo_pos ,
        "NO_EMI_DP": num_emi
    }

# DATOS INSCRIPCION
    query_datos_insc= models.datos_inscripcion.objects.filter(pk_fk_clave_catastral=datos_clav_c,tipo='ACTUAL')

    for dat_insc in query_datos_insc:
        bajo_num = dat_insc.bajo_numero
        tomo= dat_insc.tomo
        dia_ins = dat_insc.dia_i
        mes_ins = dat_insc.mes_i
        year_ins = dat_insc.año_i
        zona_ins = dat_insc.zona_i

    datos_rp = {
        "BN_ACT_DRP": bajo_num,
        "TO_ACT_DRP": tomo ,
        "DIA_ACT_DRP": dia_ins ,
        "MES_ACT_DRP": mes_ins ,
        "YEAR_ACT_DRP":year_ins ,
        "ZON_ACT_DRP": zona_ins
    }

    query_datos_insc_2= models.datos_inscripcion.objects.filter(pk_fk_clave_catastral=datos_clav_c,tipo='ANTECEDENTE')

    for dat_insc in query_datos_insc_2:
        bajo_num = dat_insc.bajo_numero
        tomo= dat_insc.tomo
        dia_ins = dat_insc.dia_i
        mes_ins = dat_insc.mes_i
        year_ins = dat_insc.año_i
        zona_ins = dat_insc.zona_i

    datos_rp_2 = {
        "BN_ANTE_DRP": bajo_num,
        "TO_ANTE_DRP": tomo ,
        "DIA_ANTE_DRP": dia_ins ,
        "MES_ANTE_DRP": mes_ins ,
        "YEAR_ANTE_DRP":year_ins ,
        "ZON_ANTE_DRP": zona_ins
    }

    datos_rp.update(datos_rp_2)

# DATOS TERRENOS RURALES ################
    query_datos_tr = models.terrenos_rurales.objects.filter(pk_fk_clave_catastral=datos_clav_c)

    if len(query_datos_tr)==1:
        info_f1=query_datos_tr[0]

        datos_tr={
        "TIP_SUE_TR_1":info_f1.tipo_suelo,
        "VAL_HAS_TR_1":info_f1.valor_has,
        "HAS_TR_1":info_f1.sup_has,
        "A_TR_1":info_f1.a,
        "C_TR_1":info_f1.c,
        "TOP_TR":info_f1.top,
        "VIAS_TR":info_f1.vias_c,

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
    
    if len(query_datos_tr)>=2:
        info_f1=query_datos_tr[0]
        info_f2=query_datos_tr[1]

        datos_tr={
        "TIP_SUE_TR_1":info_f1.tipo_suelo,
        "VAL_HAS_TR_1":info_f1.valor_has,
        "HAS_TR_1":info_f1.sup_has,
        "A_TR_1":info_f1.a,
        "C_TR_1":info_f1.c,
        "TOP_TR":info_f1.top,
        "VIAS_TR":info_f1.vias_c,

        "TIP_SUE_TR_2":info_f2.tipo_suelo,
        "VAL_HAS_TR_2":info_f2.valor_has,
        "HAS_TR_2":info_f2.a,
        "A_TR_2":info_f2.a,
        "C_TR_2":info_f2.c,

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
    
    if len(query_datos_tr)>=3:
        info_f1=query_datos_tr[0]
        info_f2=query_datos_tr[1]
        info_f3=query_datos_tr[2]

        datos_tr={
        "TIP_SUE_TR_1":info_f1.tipo_suelo,
        "VAL_HAS_TR_1":info_f1.valor_has,
        "HAS_TR_1":info_f1.sup_has,
        "A_TR_1":info_f1.a,
        "C_TR_1":info_f1.c,
        "TOP_TR":info_f1.top,
        "VIAS_TR":info_f1.vias_c,

        "TIP_SUE_TR_2":info_f2.tipo_suelo,
        "VAL_HAS_TR_2":info_f2.valor_has,
        "HAS_TR_2":info_f2.a,
        "A_TR_2":info_f2.a,
        "C_TR_2":info_f2.c,

        "TIP_SUE_TR_3":info_f3.tipo_suelo,
        "VAL_HAS_TR_3":info_f3.valor_has,
        "HAS_TR_3":info_f3.a,
        "A_TR_3":info_f3.a,
        "C_TR_3":info_f3.c,

        "TIP_SUE_TR_4":'',
        "VAL_HAS_TR_4":'',
        "HAS_TR_4":'',
        "A_TR_4":'',
        "C_TR_4":''

        }
    
    if len(query_datos_tr)>=4:
        info_f1=query_datos_tr[0]
        info_f2=query_datos_tr[1]
        info_f3=query_datos_tr[2]
        info_f4=query_datos_tr[3]

        datos_tr={
        "TIP_SUE_TR_1":info_f1.tipo_suelo,
        "VAL_HAS_TR_1":info_f1.valor_has,
        "HAS_TR_1":info_f1.sup_has,
        "A_TR_1":info_f1.a,
        "C_TR_1":info_f1.c,
        "TOP_TR":info_f1.top,
        "VIAS_TR":info_f1.vias_c,

        "TIP_SUE_TR_2":info_f2.tipo_suelo,
        "VAL_HAS_TR_2":info_f2.valor_has,
        "HAS_TR_2":info_f2.a,
        "A_TR_2":info_f2.a,
        "C_TR_2":info_f2.c,

        "TIP_SUE_TR_3":info_f3.tipo_suelo,
        "VAL_HAS_TR_3":info_f3.valor_has,
        "HAS_TR_3":info_f3.a,
        "A_TR_3":info_f3.a,
        "C_TR_3":info_f3.c,

        "TIP_SUE_TR_4":info_f4.tipo_suelo,
        "VAL_HAS_TR_4":info_f4.valor_has,
        "HAS_TR_4":info_f4.a,
        "A_TR_4":info_f4.a,
        "C_TR_4":info_f4.c

        }

    query_datos_tr_2 = models.terrenos_rurales_superficietotal.objects.filter(pk_fk_clave_catastral=datos_clav_c)
    for dat_tr in query_datos_tr_2:
        has_sp = dat_tr.sup_t_has
        a_sp = dat_tr.a
        c_sp = dat_tr.c


    datos_tr_2={
        # DATOS RURALES INFRAESTRUCTURA NO SE GUARDA?
        "INF_HAS_TR":'',
        "INF_A_TR":'',
        "INF_C_TR":'',

        # DATOS RURALES SUPERFICIA AGOSTADERO TAMPOCO?
        "SUP_AG_HAS_TR":'',
        "SUP_AG_A_TR":'',
        "SUP_AG_C_TR":'',

        # SUPERFICIE TOTAL
        "SUP_T_HAS_TR":has_sp,
        "SUP_T_A_TR":a_sp,
        "SUP_T_C_TR":c_sp,
    }

    datos_tr.update(datos_tr_2)
    

# DATOS TERRENOS URBANOS Y SUBURBANOS

    query_datos_us = models.terrenos_urbanos_suburbanos.objects.filter(fk_clave_catastral=datos_clav_c)

    if len(query_datos_us)==1:
        info_us_1=query_datos_us[0]

        datos_us={
        "VAL_M2_DUS":info_us_1.valor_m2,
        "ARE_TER_DUS":info_us_1.area,
        
        "T_C_DUS_1":info_us_1.c,
        "T_VAL_M2_DUS_1":info_us_1.valor,
        "T_FRE_DUS_1":info_us_1.frente,
        "T_PROF_DUS_1":info_us_1.profundidad,

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
        
    if len(query_datos_us)>=2:
        info_us_1=query_datos_us[0]
        info_us_2=query_datos_us[1]

        datos_us={
        "VAL_M2_DUS":info_us_1.valor_m2,
        "ARE_TER_DUS":info_us_1.area,

        "T_C_DUS_1":info_us_1.c,
        "T_VAL_M2_DUS_1":info_us_1.valor,
        "T_FRE_DUS_1":info_us_1.frente,
        "T_PROF_DUS_1":info_us_1.profundidad,

        "T_C_DUS_2":info_us_2.c,
        "T_VAL_M2_DUS_2":info_us_2.valor,
        "T_FRE_DUS_2":info_us_2.frente,
        "T_PROF_DUS_2":info_us_2.profundidad,


        "T_C_DUS_3":'',
        "T_VAL_M2_DUS_3":'',
        "T_FRE_DUS_3":'',
        "T_PROF_DUS_3":'',

        "T_C_DUS_4":'',
        "T_VAL_M2_DUS_4":'',
        "T_FRE_DUS_4":'',
        "T_PROF_DUS_4":''

    }
        
    if len(query_datos_us)>=3:
        info_us_1=query_datos_us[0]
        info_us_2=query_datos_us[1]
        info_us_3=query_datos_us[2]

        datos_us={
        "VAL_M2_DUS":info_us_1.valor_m2,
        "ARE_TER_DUS":info_us_1.area,

        "T_C_DUS_1":info_us_1.c,
        "T_VAL_M2_DUS_1":info_us_1.valor,
        "T_FRE_DUS_1":info_us_1.frente,
        "T_PROF_DUS_1":info_us_1.profundidad,

        "T_C_DUS_2":info_us_2.c,
        "T_VAL_M2_DUS_2":info_us_2.valor,
        "T_FRE_DUS_2":info_us_2.frente,
        "T_PROF_DUS_2":info_us_2.profundidad,


        "T_C_DUS_3":info_us_3.c,
        "T_VAL_M2_DUS_3":info_us_3.valor,
        "T_FRE_DUS_3":info_us_3.frente,
        "T_PROF_DUS_3":info_us_3.profundidad,

        "T_C_DUS_4":'',
        "T_VAL_M2_DUS_4":'',
        "T_FRE_DUS_4":'',
        "T_PROF_DUS_4":''

    }
        
    if len(query_datos_us)>=4:
        info_us_1=query_datos_us[0]
        info_us_2=query_datos_us[1]
        info_us_3=query_datos_us[2]
        info_us_4=query_datos_us[3]

        datos_us={
        "VAL_M2_DUS":info_us_1.valor_m2,
        "ARE_TER_DUS":info_us_1.area,

        "T_C_DUS_1":info_us_1.c,
        "T_VAL_M2_DUS_1":info_us_1.valor,
        "T_FRE_DUS_1":info_us_1.frente,
        "T_PROF_DUS_1":info_us_1.profundidad,

        "T_C_DUS_2":info_us_2.c,
        "T_VAL_M2_DUS_2":info_us_2.valor,
        "T_FRE_DUS_2":info_us_2.frente,
        "T_PROF_DUS_2":info_us_2.profundidad,


        "T_C_DUS_3":info_us_3.c,
        "T_VAL_M2_DUS_3":info_us_3.valor,
        "T_FRE_DUS_3":info_us_3.frente,
        "T_PROF_DUS_3":info_us_3.profundidad,

        "T_C_DUS_4":info_us_4.c,
        "T_VAL_M2_DUS_4":info_us_4.valor,
        "T_FRE_DUS_4":info_us_4.frente,
        "T_PROF_DUS_4":info_us_4.profundidad

    }

    
    # DEMERITOS PREDIOS URBANOS
    query_datos_us_dpu_1 = models.demeritos_predios_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,descripcion='Interés Social')

    for dat_us in query_datos_us_dpu_1:
        valor_is=dat_us.valor

    query_datos_us_dpu_2 = models.demeritos_predios_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,descripcion='Excedente de área')

    for dat_us in query_datos_us_dpu_2:
        valor_ex_a=dat_us.valor

    query_datos_us_dpu_3 = models.demeritos_predios_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,descripcion='Topografía')

    for dat_us in query_datos_us_dpu_3:
        valor_topo=dat_us.valor
    
    query_datos_us_dpu_4 = models.demeritos_predios_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,descripcion='Cond. Física imprevista')

    for dat_us in query_datos_us_dpu_4:
        valor_cond_f=dat_us.valor

    
    # INCREMENTO POR ESQUINA

    query_datos_us_inc_1 = models.incrementos_esquina_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,tipo='A')

    for dat_inc in query_datos_us_inc_1:
        valor_A=dat_inc.valor

    query_datos_us_inc_2 = models.incrementos_esquina_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,tipo='B')

    for dat_inc in query_datos_us_inc_2:
        valor_B=dat_inc.valor

    query_datos_us_inc_3 = models.incrementos_esquina_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,tipo='C')

    for dat_inc in query_datos_us_inc_3:
        valor_C=dat_inc.valor
    
    query_datos_us_inc_4 = models.incrementos_esquina_urbanos.objects.filter(fk_clave_catastral=datos_clav_c,tipo='D')

    for dat_inc in query_datos_us_inc_4:
        valor_D=dat_inc.valor

    datos_us_2={
        "DEM_INT_SOC_DUS":valor_is,
        "DEM_EXC_ARE_DUS":valor_ex_a,
        "DEM_TOPO_DUS":valor_topo,
        "DEM_COND_FIS_DUS":valor_cond_f,

        "INC_X_ESQ_DUS_A":valor_A,
        "INC_X_ESQ_DUS_B":valor_B,
        "INC_X_ESQ_DUS_C":valor_C,
        "INC_X_ESQ_DUS_D":valor_D
    }

    datos_us.update(datos_us_2)

    # DATOS CONSTRUCCIONES

    query_datos_cons = models.ficha_datos_construcciones.objects.filter(fk_clave_catastral=datos_clav_c)

    if len(query_datos_cons)==1:
        info_cons_1=query_datos_cons[0]

        datos_const={
        "DAT_C_TIPO_A":info_cons_1.tipo_c,
        "DAT_C_EDO_A":info_cons_1.est,
        "DAT_C_T_A":info_cons_1.terreno,
        "DAT_C_ANT_A":info_cons_1.antiguedad,
        "DAT_C_ARE_M2_A":info_cons_1.area_c,

        "DAT_C_TIPO_B":'',
        "DAT_C_EDO_B":'',
        "DAT_C_T_B":'',
        "DAT_C_ANT_B":'',
        "DAT_C_ARE_M2_B":'',

        "DAT_C_TIPO_C":'',
        "DAT_C_EDO_C":'',
        "DAT_C_T_C":'',
        "DAT_C_ANT_C":'',
        "DAT_C_ARE_M2_C":'',

        "DAT_C_TIPO_D":'',
        "DAT_C_EDO_D":'',
        "DAT_C_T_D":'',
        "DAT_C_ANT_D":'',
        "DAT_C_ARE_M2_D":'',

        "DAT_C_TIPO_E":'',
        "DAT_C_EDO_E":'',
        "DAT_C_T_E":'',
        "DAT_C_ANT_E":'',
        "DAT_C_ARE_M2_E":''
    }
        
    if len(query_datos_cons)>=2:
        info_cons_1=query_datos_cons[0]
        info_cons_2=query_datos_cons[1]

        datos_const={
        "DAT_C_TIPO_A":info_cons_1.tipo_c,
        "DAT_C_EDO_A":info_cons_1.est,
        "DAT_C_T_A":info_cons_1.terreno,
        "DAT_C_ANT_A":info_cons_1.antiguedad,
        "DAT_C_ARE_M2_A":info_cons_1.area_c,

        "DAT_C_TIPO_B":info_cons_2.tipo_c,
        "DAT_C_EDO_B":info_cons_2.est,
        "DAT_C_T_B":info_cons_2.terreno,
        "DAT_C_ANT_B":info_cons_2.antiguedad,
        "DAT_C_ARE_M2_B":info_cons_2.area_c,

        "DAT_C_TIPO_C":'',
        "DAT_C_EDO_C":'',
        "DAT_C_T_C":'',
        "DAT_C_ANT_C":'',
        "DAT_C_ARE_M2_C":'',

        "DAT_C_TIPO_D":'',
        "DAT_C_EDO_D":'',
        "DAT_C_T_D":'',
        "DAT_C_ANT_D":'',
        "DAT_C_ARE_M2_D":'',

        "DAT_C_TIPO_E":'',
        "DAT_C_EDO_E":'',
        "DAT_C_T_E":'',
        "DAT_C_ANT_E":'',
        "DAT_C_ARE_M2_E":''
    }
        
    if len(query_datos_cons)>=3:
        info_cons_1=query_datos_cons[0]
        info_cons_2=query_datos_cons[1]
        info_cons_3=query_datos_cons[2]

        datos_const={
        "DAT_C_TIPO_A":info_cons_1.tipo_c,
        "DAT_C_EDO_A":info_cons_1.est,
        "DAT_C_T_A":info_cons_1.terreno,
        "DAT_C_ANT_A":info_cons_1.antiguedad,
        "DAT_C_ARE_M2_A":info_cons_1.area_c,

        "DAT_C_TIPO_B":info_cons_3.tipo_c,
        "DAT_C_EDO_B":info_cons_3.est,
        "DAT_C_T_B":info_cons_3.terreno,
        "DAT_C_ANT_B":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_B":info_cons_3.area_c,

        "DAT_C_TIPO_C":info_cons_3.tipo_c,
        "DAT_C_EDO_C":info_cons_3.est,
        "DAT_C_T_C":info_cons_3.terreno,
        "DAT_C_ANT_C":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_C":info_cons_3.area_c,

        "DAT_C_TIPO_D":'',
        "DAT_C_EDO_D":'',
        "DAT_C_T_D":'',
        "DAT_C_ANT_D":'',
        "DAT_C_ARE_M2_D":'',

        "DAT_C_TIPO_E":'',
        "DAT_C_EDO_E":'',
        "DAT_C_T_E":'',
        "DAT_C_ANT_E":'',
        "DAT_C_ARE_M2_E":''
    }
        
    if len(query_datos_cons)>=4:
        info_cons_1=query_datos_cons[0]
        info_cons_2=query_datos_cons[1]
        info_cons_3=query_datos_cons[2]
        info_cons_4=query_datos_cons[3]

        datos_const={
        "DAT_C_TIPO_A":info_cons_1.tipo_c,
        "DAT_C_EDO_A":info_cons_1.est,
        "DAT_C_T_A":info_cons_1.terreno,
        "DAT_C_ANT_A":info_cons_1.antiguedad,
        "DAT_C_ARE_M2_A":info_cons_1.area_c,

        "DAT_C_TIPO_B":info_cons_3.tipo_c,
        "DAT_C_EDO_B":info_cons_3.est,
        "DAT_C_T_B":info_cons_3.terreno,
        "DAT_C_ANT_B":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_B":info_cons_3.area_c,

        "DAT_C_TIPO_C":info_cons_3.tipo_c,
        "DAT_C_EDO_C":info_cons_3.est,
        "DAT_C_T_C":info_cons_3.terreno,
        "DAT_C_ANT_C":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_C":info_cons_3.area_c,

        "DAT_C_TIPO_D":info_cons_4.tipo_c,
        "DAT_C_EDO_D":info_cons_4.est,
        "DAT_C_T_D":info_cons_4.terreno,
        "DAT_C_ANT_D":info_cons_4.antiguedad,
        "DAT_C_ARE_M2_D":info_cons_4.area_c,

        "DAT_C_TIPO_E":'',
        "DAT_C_EDO_E":'',
        "DAT_C_T_E":'',
        "DAT_C_ANT_E":'',
        "DAT_C_ARE_M2_E":''
    }
        
    if len(query_datos_cons)>=5:
        info_cons_1=query_datos_cons[0]
        info_cons_2=query_datos_cons[1]
        info_cons_3=query_datos_cons[2]
        info_cons_4=query_datos_cons[3]
        info_cons_5=query_datos_cons[4]

        datos_const={
        "DAT_C_TIPO_A":info_cons_1.tipo_c,
        "DAT_C_EDO_A":info_cons_1.est,
        "DAT_C_T_A":info_cons_1.terreno,
        "DAT_C_ANT_A":info_cons_1.antiguedad,
        "DAT_C_ARE_M2_A":info_cons_1.area_c,

        "DAT_C_TIPO_B":info_cons_3.tipo_c,
        "DAT_C_EDO_B":info_cons_3.est,
        "DAT_C_T_B":info_cons_3.terreno,
        "DAT_C_ANT_B":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_B":info_cons_3.area_c,

        "DAT_C_TIPO_C":info_cons_3.tipo_c,
        "DAT_C_EDO_C":info_cons_3.est,
        "DAT_C_T_C":info_cons_3.terreno,
        "DAT_C_ANT_C":info_cons_3.antiguedad,
        "DAT_C_ARE_M2_C":info_cons_3.area_c,

        "DAT_C_TIPO_D":info_cons_4.tipo_c,
        "DAT_C_EDO_D":info_cons_4.est,
        "DAT_C_T_D":info_cons_4.terreno,
        "DAT_C_ANT_D":info_cons_4.antiguedad,
        "DAT_C_ARE_M2_D":info_cons_4.area_c,

        "DAT_C_TIPO_E":info_cons_5.tipo_c,
        "DAT_C_EDO_E":info_cons_5.est,
        "DAT_C_T_E":info_cons_5.terreno,
        "DAT_C_ANT_E":info_cons_5.antiguedad,
        "DAT_C_ARE_M2_E":info_cons_5.area_c,
    }

    # VALORES
    query_datos_val = models.valores_catastro.objects.filter(clave_catastral_pk=datos_clav_c)

    for dat_val in query_datos_val:
        val_ter = dat_val.valor_terreno
        val_const= dat_val.valor_construccion
        val_cat = dat_val.valor_catastral

    datos_const_2={
        "DAT_C_V_TER":val_ter,
        "DAT_C_VAL_CON":val_const,
        "DAT_C_VAL_CAT":val_cat
    }

    datos_const.update(datos_const_2)

    functions.reporte_ficha_cat(datos_clav_c,datos_gral,datos_doc,datos_pred,datos_rp,datos_tr,datos_us,datos_const)
    


    #aqui podrias poner la funcion que mande a llamar el reporte como lo hiciste en registrar datos inmuebles del DC017
