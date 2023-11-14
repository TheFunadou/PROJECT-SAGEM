from catastro import models as models_catastro
from catastro import functions
import os
from pyreportjasper import PyReportJasper
import json
import datetime



def crear_reporte_DC017(clave_cat,username):
    query_datos_contrib = models_catastro.Datos_Contribuyentes.objects.get(clave_catastral=clave_cat)
    query_dom_inmueble = models_catastro.Domicilio_inmueble.objects.get(pk_fk_clave_catastral_id=clave_cat)
    query_datos_inmueble = models_catastro.Datos_inmuebles.objects.get(fk_clave_catastral_id=clave_cat)
    query_datos_const = models_catastro.Datos_Construccion.objects.get(fk_clave_catastral_id=clave_cat)
    
    fecha_hora_actual = datetime.datetime.now()

    # Crear scrpit json
    data = {'data': [{
        # DATOS USUARIO
        'NOM_USER':username,
        'FECHA_HORA':fecha_hora_actual.strftime("%d/%m/%Y %H:%M"),
        
        # 008 123 456 789 123 456 789 123 456 678
        # CLAVE CATASTRAL
        'C_ZON': clave_cat[0:3],
        'C_MUN':clave_cat[3:6],
        'C_LOC': clave_cat[6:9],
        'C_REG': clave_cat[9:12],
        'C_MAN': clave_cat[12:15],
        'C_LOT': clave_cat[15:18],
        'C_NIV': clave_cat[18:21],
        'C_DP': clave_cat[21:24],
        'C_DV': clave_cat[24:27],

        # DATOS CONTRIBUYENTE
        'NOM_P': query_datos_contrib.nombre,
        'AP_P': query_datos_contrib.apaterno,
        'AM_P': query_datos_contrib.amaterno,
        'RFC': query_datos_contrib.rfc,
        'CALLE_P': query_datos_contrib.calle,
        'NUM_EXT': query_datos_contrib.num_ext,
        'NUM_INT': query_datos_contrib.num_int,
        'COL_P': query_datos_contrib.colonia_fraccionamiento,
        'LOC_P': query_datos_contrib.localidad,

        # DATOS INMUEBLE
        'CALLE_INM': query_dom_inmueble.calle,
        'NUM_EXT_INM': query_dom_inmueble.num_ext,
        'NUM_INT_INM': query_dom_inmueble.num_int,
        'COL_O_FRA_INM': query_dom_inmueble.col_fracc,
        'MUN_INM': query_dom_inmueble.localidad,

        # DETALLES INMUEBLE
        'LOC_INM': query_datos_inmueble.ciudad_localidad,
        'T_PRED_INM': query_datos_inmueble.pk_estado_fisico_predio,
        'TEN_PRED': query_datos_inmueble.tenencia_predio,
        'EST_F_PRED': query_datos_inmueble.pk_estado_fisico_predio,
        'MOD_F_C_PRED': query_datos_inmueble.modificacion_física_construccion,
        'SUP_F_PRED': f'{query_datos_inmueble.superficie_predio} m²',
        'USO_O_DEST': query_datos_inmueble.uso_predio,

        #DATOS CONSTRUCCION
        'TIPO_TECHOS': query_datos_const.techos,
        'TIPO_PISOS': query_datos_const.pisos,
        'TIPO_MUROS': query_datos_const.muros,
        'TIPO_BA': query_datos_const.tipo_baños,
        'TIPO_INST_ELEC': query_datos_const.instalacion_electrica,
        'TIPO_P_V': query_datos_const.puertas_ventanas,
        'EDAD_A': query_datos_const.edad,
        'NUM_NIV': query_datos_const.niveles,
        'A_S_C_D_N': '',
        'INVERSION': '',
        'PLANO_CROQUIS': functions.checkbox_rep(query_datos_const.plano_croquis),
        'DOC_JUST': functions.checkbox_rep(query_datos_const.doc_just_prop) ,
        'ULT_RECI': functions.checkbox_rep(query_datos_const.ult_rec_imp),
        'LIC_OBRA_DEM': functions.checkbox_rep(query_datos_const.lic_obr_dem),
        'NOM_COM_C': f'{query_datos_contrib.nombre} {query_datos_contrib.apaterno} {query_datos_contrib.amaterno}'
    }]}

    # Crear archivo.json
    crear_json = json.dumps(data)

    ruta_arch_json = 'catastro/static/reports/DC017/REPORTE_DC017.json'

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
    ruta_arch_dc017='catastro/static/reports/DC017/DC017.jrxml'

    # Archivo de salida que se almacenara en la carpeta REPORTES_CATASTRO
    arch_sal = ruta_carpeta+'/DC017_'+clave_cat

    functions.crear_reporte(ruta_arch_json,ruta_arch_dc017,arch_sal)

