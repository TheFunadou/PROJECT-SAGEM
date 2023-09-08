# Escribe tus funciones aqui

import os
from pyreportjasper import PyReportJasper
import json
import webbrowser

#FUNCION PARA DETERMINAR EL NUMERO OFICIAL DE UNA CASA
num_oficial = lambda num_ext, num_int: num_int if len(num_ext) == 0 else num_ext

#FUNCION PARA CHECKBOX PARA EL REPORTE
checkbox_rep = lambda seleccion: 'O' if seleccion == 'SI' else 'X'

def formato_clave_cat(valor):
    
    if (len(valor) == 3):
        return valor
    if (len(valor)==2):
        return f'00{valor}'
    if (len(valor) == 1):
        return f'0{valor}'

#REPORTE DC017 -- Se le pasan diccionarios como parametros para facilitar la insercion de datos
def crear_reporte_p(datos_clav_c,datos_contribuyente,datos_inm,detalles_inm,datos_cons):
    # Crear scrpit json
    datos = {'datos': [{
        # DATOS USUARIO
        

        # CLAVE CATASTRAL
        'C_ZON': datos_clav_c['zona_cat'],
        'C_MUN': datos_clav_c['mun'],
        'C_LOC': datos_clav_c['loc'],
        'C_REG': datos_clav_c['reg'],
        'C_MAN': datos_clav_c['man'],
        'C_LOT': datos_clav_c['lot'],
        'C_NIV': datos_clav_c['niv'],
        'C_DP': datos_clav_c['dep'],
        'C_DV': datos_clav_c['dv'],

        # DATOS CONTRIBUYENTE
        'NOM_P': datos_contribuyente['nombre'],
        'AP_P': datos_contribuyente['ap'],
        'AM_P': datos_contribuyente['am'],
        'RFC': datos_contribuyente['rfc'],
        'CALLE_P': datos_contribuyente['calle'],
        'NUM_O_P': datos_contribuyente['num_ofi'],
        'COL_P': datos_contribuyente['col_fracc'],
        'LOC_P': 'Minatitlan',

        # DATOS INMUEBLE
        'CALLE_INM': datos_inm['calle'],
        'NUM_O_INM': datos_inm['num_ofi'],
        'COL_O_FRA_INM': datos_inm['col_fracc'],
        'MUN_INM': detalles_inm['mun'],

        # DETALLES INMUEBLE
        'LOC_INM': 'Minatitlan',
        'T_PRED_INM': detalles_inm['tp_pred'],
        'TEN_PRED': detalles_inm['tenen'],
        'EST_F_PRED': detalles_inm['estado_fis'],
        'MOD_F_C_PRED': detalles_inm['mod_f'],
        'SUP_F_PRED': detalles_inm['sup'],
        'USO_O_DEST': detalles_inm['uso_d'],

        #DATOS CONSTRUCCION
        'TIPO_TECHOS': datos_cons['techos'],
        'TIPO_PISOS': datos_cons['pisos'],
        'TIPO_MUROS': datos_cons['muros'],
        'TIPO_BA': datos_cons['tp_ba'],
        'TIPO_INST_ELEC': datos_cons['inst_e'],
        'TIPO_P_V': datos_cons['puertas_v'],
        'EDAD_A': datos_cons['edad'],
        'NUM_NIV': datos_cons['niv'],
        'A_S_C_D_N': '',
        'INVERSION': '',
        'PLANO_CROQUIS': datos_cons['pla_cro'],
        'DOC_JUST': datos_cons['doc_jus'],
        'ULT_RECI': datos_cons['ult_rec'],
        'LIC_OBRA_DEM': datos_cons['lic_obr'],
        'NOM_COM_C': datos_contribuyente['nombre']+" "+datos_contribuyente['ap'] +" "+  datos_contribuyente['am']
    }]}

    # Crear archivo.json
    crear_json = json.dumps(datos)

    # Establecer ruta y nombre de archivo.json
    arch_json='REPORTE_DC017.json'
    ruta_json = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_json = os.path.join(ruta_json, 'static' ,'reports', 'DC017', arch_json)

    # Cargar scrpit al archivo.json
    with open(ruta_archivo_json, "w", encoding="cp1250") as file:
        file.write(crear_json)
    file.close

    # Ruta carpeta documentos en One Drive
    ruta_carpeta = os.path.join(
        os.path.expanduser("~"), "OneDrive", "Documentos")
    ruta_carpeta = ruta_carpeta+'\REPORTES_CATASTRO'
    ruta_carpeta = ruta_carpeta.replace('\\', '/')

    # Buscar si existe una carpeta REPORTES_CATASTRO de lo contrario crearla
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    # Archivo de entrada jrxml
    arch_jrxml='R_DC017.jrxml'
    ruta_jrxml = os.path.dirname(os.path.abspath(__file__))
    arch_ent = os.path.join(ruta_jrxml,'static' ,'reports', 'DC017', arch_jrxml)

    # Archivo de salida que se almacenara en la carpeta REPORTES_CATASTRO
    arch_sal = ruta_carpeta+'/DC017_'+datos_contribuyente["clave_catastral"]

    crear_reporte(ruta_archivo_json,arch_ent,arch_sal)

#REPORTE FICHA CATASTRAL
def reporte_ficha_cat(datos_clav_c,datos_gral,datos_doc,datos_pred,datos_rp,datos_tr,datos_us,datos_const):
    # Crear scrpit json
    datos = {'datos': [{
        # DAT_DOC
        'TP_MOV':'',
        'TIP_PRED':'',
        'FOLIO':'',
        'DIA':'',
        'MES':'',
        'YEAR':'',

        # CLAVE CATASTRAL
        

        # DATOS CONTRIBUYENTE
        'NOM_GRAL': datos_gral['NOM_GRAL'],
        'AP_GRAL': datos_gral['AP_GRAL'],
        'AM_GRAL': datos_gral['AM_GRAL'],
        'RFC_GRAL': datos_gral['RFC_GRAL'],

        # UBIACION DEL PREDIO
        'CALL_INM_GRAL': datos_gral['CALL_INM_GRAL'],
        'NUM_O_GRAL': datos_gral['NUM_O_GRAL'],
        'COL_FRA_GRAL': datos_gral['COL_FRA_GRAL'],

        # USO O DESTINO DEL PREDIO
        'USO_DES_GRAL': datos_gral['USO_DES_GRAL'],

        #DOMICILIO PARA RECIBIR NOTIFICACIONES
        'CALLE_N': datos_gral['CALLE_N'],
        'NUM_O_INM_N': datos_gral['NUM_O_INM_N'],
        'COD_POS_N': datos_gral['COD_POS_N'],
        'COL_O_FRA_INM_N': datos_gral['COL_O_FRA_INM_N'],
        'CIUDAD_N': 'MINATITLAN, VER',

        #DATOS DEL DOCUMENTO DE PROPIEDAD O POSESION
        'LUG_EXP_DOC':datos_doc['LUG_EXP_DOC'],
        'TD_DOC': datos_doc['TD_DOC'],
        'NUM_DOC':datos_doc['NUM_DOC'],
        'DIA_DOC': datos_doc['DIA_DOC'],
        'MES_DOC':datos_doc['MES_DOC'],
        'YEAR_DOC': datos_doc['YEAR_DOC'],
        'NOT_DOC':datos_doc['NOT_DOC'],

        #DATOS DEL PREDIO
        'TIP_AVA_DP':datos_pred['TIP_AVA_DP'],
        'FRAC_DP':datos_pred['FRAC_DP'],
        'TRAS_DOM_DP':datos_pred['TRAS_DOM_DP'],
        'REG_LEG_DP':datos_pred['REG_LEG_DP'],
        'TEN_DP':datos_pred['TEN_DP'],
        'EST_FIS_DP':datos_pred['EST_FIS_DP'],
        'COD_USO_DP':datos_pred['COD_USO_DP'],
        'TIP_POS_DP':datos_pred['TIP_POS_DP'],
        'NO_EMI_DP':datos_pred['NO_EMI_DP'],

        #DATOS DE INSCRIPCION EN EL REGISTRO PUBLICO DE LA PROPIEDAD
        'BN_ACT_DRP':datos_rp['BN_ACT_DRP'],
        'BN_ANTE_DRP':datos_rp['BN_ANTE_DRP'],
        'TO_ACT_DRP':datos_rp['TO_ACT_DRP'],
        'TO_ANTE_DRP':datos_rp['TO_ANTE_DRP'],
        'DIA_ACT_DRP':datos_rp['DIA_ACT_DRP'],
        'DIA_ANTE_DRP':datos_rp['DIA_ANTE_DRP'],
        'MES_ACT_DRP':datos_rp['MES_ACT_DRP'],
        'MES_ANTE_DRP':datos_rp['MES_ANTE_DRP'],
        'YEAR_ACT_DRP':datos_rp['YEAR_ACT_DRP'],
        'YEAR_ANTE_DRP':datos_rp['YEAR_ANTE_DRP'],
        'ZON_ACT_DRP':datos_rp['ZON_ACT_DRP'],
        'ZON_ANTE_DRP':datos_rp['ZON_ANTE_DRP'],

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

        'INF_HAS_TR':datos_tr['INF_HAS_TR'],
        'INF_A_TR':datos_tr['INF_A_TR'],
        'INF_C_TR':datos_tr['INF_C_TR'],

        'SUP_AG_HAS_TR':datos_tr['SUP_AG_HAS_TR'],
        'SUP_AG_A_TR':datos_tr['SUP_AG_A_TR'],
        'SUP_AG_C_TR':datos_tr['SUP_AG_C_TR'],

        'SUP_T_HAS_TR':datos_tr['SUP_T_HAS_TR'],
        'SUP_T_A_TR':datos_tr['SUP_T_A_TR'],
        'SUP_T_C_TR':datos_tr['SUP_T_C_TR'],

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

        'INC_X_ESQ_DUS_A':datos_us['INC_X_ESQ_DUS_A'],
        'INC_X_ESQ_DUS_B':datos_us['INC_X_ESQ_DUS_B'],
        'INC_X_ESQ_DUS_C':datos_us['INC_X_ESQ_DUS_C'],
        'INC_X_ESQ_DUS_D':datos_us['INC_X_ESQ_DUS_D'],

        'DEM_INT_SOC_DUS':datos_us['DEM_INT_SOC_DUS'],
        'DEM_EXC_ARE_DUS':datos_us['DEM_EXC_ARE_DUS'],
        'DEM_TOPO_DUS':datos_us['DEM_TOPO_DUS'],
        'DEM_COND_FIS_DUS':datos_us['DEM_COND_FIS_DUS'],

        # DATOS CONSTRUCCIONES

        'DAT_C_TIPO_A':datos_const['DAT_C_TIPO_A'],
        'DAT_C_EDO_A':datos_const['DAT_C_EDO_A'],
        'DAT_C_T_A':datos_const['DAT_C_T_A'],
        'DAT_C_ANT_A':datos_const['DAT_C_ANT_A'],
        'DAT_C_ARE_M2_A':datos_const['DAT_C_ARE_M2_A'],

        'DAT_C_TIPO_B':datos_const['DAT_C_TIPO_B'],
        'DAT_C_EDO_B':datos_const['DAT_C_EDO_B'],
        'DAT_C_T_B':datos_const['DAT_C_T_B'],
        'DAT_C_ANT_B':datos_const['DAT_C_ANT_B'],
        'DAT_C_ARE_M2_B':datos_const['DAT_C_ARE_M2_B'],

        'DAT_C_TIPO_C':datos_const['DAT_C_TIPO_C'],
        'DAT_C_EDO_C':datos_const['DAT_C_EDO_C'],
        'DAT_C_T_C':datos_const['DAT_C_T_C'],
        'DAT_C_ANT_C':datos_const['DAT_C_ANT_C'],
        'DAT_C_ARE_M2_C':datos_const['DAT_C_ARE_M2_C'],

        'DAT_C_TIPO_D':datos_const['DAT_C_TIPO_D'],
        'DAT_C_EDO_D':datos_const['DAT_C_EDO_D'],
        'DAT_C_T_D':datos_const['DAT_C_T_D'],
        'DAT_C_ANT_D':datos_const['DAT_C_ANT_D'],
        'DAT_C_ARE_M2_D':datos_const['DAT_C_ARE_M2_D'],

        'DAT_C_TIPO_E':datos_const['DAT_C_TIPO_E'],
        'DAT_C_EDO_E':datos_const['DAT_C_EDO_E'],
        'DAT_C_T_E':datos_const['DAT_C_T_E'],
        'DAT_C_ANT_E':datos_const['DAT_C_ANT_E'],
        'DAT_C_ARE_M2_E':datos_const['DAT_C_ARE_M2_E'],

        'DAT_C_V_TER':datos_const['DAT_C_V_TER'],
        'DAT_C_VAL_CON':datos_const['DAT_C_VAL_CON'],
        'DAT_C_VAL_CAT':datos_const['DAT_C_VAL_CAT'],
        
        'ELABORO':'',
        'TITULAR_CAT':'LIC.JOSSELINE GUTIERREZ ESPINOSA'
    }]}

    # Crear archivo.json
    crear_json = json.dumps(datos)

    # Establecer ruta y nombre de archivo.json
    arch_json='FICHA_CATASTRAL.json'
    ruta_json = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_json = os.path.join(ruta_json, 'static', 'reports', arch_json)

    # Cargar scrpit al archivo.json
    with open(ruta_archivo_json, "w", encoding="cp1250") as file:
        file.write(crear_json)
    file.close

    # Ruta carpeta documentos en One Drive
    ruta_carpeta = os.path.join(
        os.path.expanduser("~"), "OneDrive", "Documentos")
    ruta_carpeta = ruta_carpeta+'\REPORTES_CATASTRO\FICHA_CATASTRAL'
    ruta_carpeta = ruta_carpeta.replace('\\', '/')

    # Buscar si existe una carpeta REPORTES_CATASTRO de lo contrario crearla
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    # Archivo de entrada jrxml
    arch_jrxml='FICHA_CATASTRAL_MK2.jrxml'
    ruta_jrxml = os.path.dirname(os.path.abspath(__file__))
    arch_ent = os.path.join(ruta_jrxml, 'static', 'reports','FICHA_CAT', arch_jrxml)

    # Archivo de salida que se almacenara en la carpeta REPORTES_CATASTRO
    arch_sal = ruta_carpeta+'/FICHA_CATRASTRAL_'+datos_clav_c["clave_cat"]

    crear_reporte(ruta_archivo_json,arch_ent,arch_sal)




    
# CREAR REPORTE
def crear_reporte(ruta_archivo_json,arch_ent,arch_sal):
        # Conexion con la hoja json
        conn = {
        'driver': 'json',
        'data_file': ruta_archivo_json,
        'json_query': 'data'
        }

        # Crear el reporte con PyReportJasper
        pyreportjasper = PyReportJasper()
        # Configuracion del reporte
        pyreportjasper.config(
            input_file=arch_ent,
            output_file=arch_sal,
            output_formats=['pdf'],
            locale='es_MX',
            db_connection=conn)

        # Creacion del reporte
        pyreportjasper.process_report()

        # Abrir el archivo en el navegador
        webbrowser.open_new_tab(arch_sal+'.pdf')


