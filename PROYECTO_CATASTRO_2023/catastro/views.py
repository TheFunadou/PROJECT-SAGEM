from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.urls import *
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
# CREATE VIEW PARA GENERAR UNA CLASE PARA GUARDAR DATOS
from django.views.generic import CreateView
from notify import models as notify_models
#TABLA USUARIOS
from django.contrib.auth.models import User, Group

#APLICACION CATASTRO
from catastro import models
from catastro.models import Datos_Contribuyentes,Domicilio_inmueble
from catastro import functions

#DJANGO NOTIFICACIONS

# channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#consultas filtradas
from django.db.models import Q






# CERRAR SESION NO LE QUITEN EL REQUEST QUE NO JALA XD
def cerrar_sesion(request):
    return redirect('logout')


"""
#Funcion en testeo
    def acceso_catastro(request):
    
    try:
        if request.user.is_authenticated:
            #Si es verdadero
            #Obtener el grupo al que pertenece el usuario
            grupo_user = request.user.groups.filter().first()
            if grupo_user:
                nom_grupo = grupo_user.name
                
            nom_grupo.lower()    
            nom_app = request.resolver_match.app_name
            
            if (nom_grupo != nom_app):
                if request.user.is_superuser:
                    return redirect(f'{nom_grupo}:perfil_su_{nom_grupo}')
                else:
                    return redirect(f'{nom_grupo}:perfil_{nom_grupo}')   
            
    except (Group.DoesNotExist):
        HttpResponse('El usuario no pertenece actualmente a ningun grupo')

"""
    

# Create your views here.
@login_required(login_url="pag_login")
def perfil_catastro(request):
    """
    
    """
    #REDIRECCIONAR A USUARIO QUE NO PERTENEZCAN A ESE DEPARTAMENTO
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_su_catastro')
                ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx={
        'url_pag': 'x',
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO CATASTRO'
    }
    
    return render(request,'catastro/inicio_catastro.html',ctx)


# PERFIL SUPERUSUARIO

@login_required(login_url="pag_login")
def perfil_sup_user_catastro(request):
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
            ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_catastro')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx = {
        'notficaciones':'Notification.objects.values("description").filter()',
        'nom_pag': 'Catastro',
        'titulo_pag': 'INICIO SUPER USUARIO CATASTRO',
        'nombre_user': request.user.username
    }

    return render(request, 'catastro/inicio_sup_user_catastro.html', ctx)


# Pantalla 
@login_required(login_url="pag_login")
def view_registrar_usuario(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
            ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
            
    
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'REGISTRO DE USUARIOS'
    }
    
    return render(request, 'catastro/registrar_usuario.html', ctx)

# RECIBIR DATOS DE LA VIEW REGISTRAR USUARIO
@login_required(login_url='pag_login')
def registrar_usuario(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    conf_password = request.POST['conf_password']
    departamento = request.POST['departamento']
    rol = request.POST['rol']
    
    # Crear nuevo usuario
    new_user= User(username=username, email=email)
    new_user.set_password(conf_password)
    
    if(rol == 'STAFF'):
        new_user.save()
    elif(rol == 'SUPER_USUARIO'):
        new_user.is_superuser=True
        new_user.save()
    
    # Asginar un grupo al usuario
    usuario = User.objects.get(username=username)
    grupo = Group.objects.get(name=departamento)
    
    usuario.groups.add(grupo)
    
    
@login_required(login_url="pag_login")
def views_cambiar_password(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
            ### DEMAS IF DE PERFILES DE SUPER USUARIO
        else:
            if request.user.groups.filter()[0].name == 'CATASTRO':
                return redirect('catastro:perfil_cat')
            elif request.user.groups.filter()[0].name == 'FINANZAS':
                return redirect('finanzas:perfil_fin')
            elif request.user.groups.filter()[0].name == 'DESARROLLO_URBANO':
                return redirect('desarrollo_urbano:perfil_du')
    
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'RECUPERAR CONTRASEÑA'
    }
    
    return render(request, 'catastro/cambiar_password', ctx)


def vista_index_contribuyente(request):
    return render(request,'catastro/index_contribuyente.html')
#vista registro ciudadano
@login_required(login_url="pag_login")
def contribuyente_index(request):
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'REGISTRO DE CIUDADANO',
    }
    return render(request,'catastro/alta_contribuyentes.html', ctx)

#REGISTRAR DATOS DEL CIUDADANO
def registro_contribuyente(request):
    tipo_persona = request.POST['zonacat']
    tipo_identificacion = request.POST['muni']
    num_identificacion = request.POST['loc']
    nombre_razon = request.POST['region']
    apaterno = request.POST['manzana']
    amaterno = request.POST['lote']
    rfc = request.POST['nivel']
    curp = request.POST['depto']
    finado = request.POST['dvs']
    fecha_naciemiento_registro = request.POST['zonacat']
    telefono = request.POST['muni']
    celular = request.POST['loc']
    email = request.POST['region']
    observaciones = request.POST['manzana']

def registro_domicilio_contribuyente(request):
    tipo_persona = request.POST['zonacat']
    mun = request.POST['muni']
    loc = request.POST['loc']
    reg = request.POST['region']
    man = request.POST['manzana']
    lot = request.POST['lote']
    niv = request.POST['nivel']
    dep = request.POST['depto']
    dv = request.POST['dvs']

@login_required(login_url="pag_login")
def predios_index(request):
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'ALTA DE PREDIO',
    }
    return render(request,'catastro/alta_predios.html', ctx)




@login_required(login_url="pag_login")
#vista solicitud dc017
def solicitud_dc017(request):
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'SOLICITUD DC017',
    }
    return render(request,'catastro/solicitud_dc017.html', ctx)


def registrar_solicitud_dc017(request):

  
    zoncat = request.POST['zonacat']
    mun = request.POST['muni']
    loc = request.POST['loc']
    reg = request.POST['region']
    man = request.POST['manzana']
    lot = request.POST['lote']
    niv = request.POST['nivel']
    dep = request.POST['depto']
    dv = request.POST['dvs']
    
    clave_catastral = zoncat + mun + loc + reg + man + lot + niv + dep + dv

    d_clave_cat = {
        "zona_cat" : zoncat,
        "mun" : mun,
        "loc" : loc,
        "reg" : reg,
        "man" : man,
        "lot" : lot,
        "niv" : niv,
        "dep" : dep,
        "dv" : dv,
        
        "clave_cat":clave_catastral
    }

   
    apaterno = request.POST['apaterno']
    amaterno = request.POST['amaterno']
    nombre = request.POST['nombre']
    rfc = request.POST['rfc']
    telefono = request.POST['telefono']
    tipo = request.POST.get('tipo_tel')
    calle = request.POST['calle']
    colonia_fraccionamiento = request.POST['colonia_fraccionamiento']
    num_int = request.POST['num_int']
    num_ext = request.POST['num_ext']
    localidad = request.POST['localidad']
    codigo_postal = request.POST['codigo_postal']

    ob = models.Datos_Contribuyentes.objects.create(
        clave_catastral=clave_catastral,
        rfc=rfc,
        nombre=nombre,
        apaterno=apaterno,
        amaterno=amaterno,
        telefono=telefono,
        tipo=tipo,
        calle=calle,
        num_int=num_int,
        num_ext=num_ext,
        colonia_fraccionamiento=colonia_fraccionamiento,
        localidad=localidad,
        codigo_postal=codigo_postal)
    
    
    # Hacemos un llamado a la función domicilio inmueble para que se ejecute a la par con los datos del contribuyente y asi almacene los datos.
    return domicilio_inmueble(request, d_clave_cat)

# REGISTRO DEL DOMICILIO DEL INMUEBLE
def domicilio_inmueble(request, d_clave_cat):
   
    calle = request.POST['calle2']
    col_fracc = request.POST['col_fracc']
    num_int = request.POST['ni']
    num_ext=request.POST['ne']
    localidad = request.POST['localidad']

    models.Domicilio_inmueble.objects.create(
        pk_fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=d_clave_cat["clave_cat"]),
        calle=calle,
        num_int=num_int,
        num_ext=num_ext,
        col_fracc=col_fracc,
        localidad=localidad
    )

    return registrar_datos_inmueble(request, d_clave_cat)

# REGISTRAR DATOS DEL INMUEBLE
def registrar_datos_inmueble(request, pk_fk_clave_catastral_id):

   
    

    clave_catastral =pk_fk_clave_catastral_id

    d_clave_cat_i = {
        "clave_cat": clave_catastral,
        
    }

    #DATOS DEL INMUEBLE
    estado_fisico = request.POST['estadofisico']
    tipo_predios = request.POST['tipopredio']
    tenencia_predios = request.POST['tenenciapredio']
    modificacion_fisica = request.POST['modificacion']
    superficie = request.POST['superficie']
    municipio = request.POST['municipio2']
    ciudad = request.POST['ciudad2']
    uso_destino = request.POST['uso']

    #DATOS DE LA CONSTRUCCION
    techos = request.POST['techos']
    pisos = request.POST['pisos']
    muros = request.POST['muros']
    tipo_baños = request.POST['tipobaño']
    instalacion_electrica = request.POST['instalacionelectrica']
    puertas_ventanas = request.POST['puertaventana']
    edad_años = request.POST['años']
    niveles = request.POST['niveles']
    plan_croq= 'SI' if 'P_O_C' in request.POST else 'NO'
    doc_just= 'SI' if 'DOC_JUST' in request.POST else 'NO'
    ult_rec= 'SI' if 'U_R_I' in request.POST else 'NO'
    lic_obr= 'SI' if 'LIC_OB' in request.POST else 'NO'
    

    models.Datos_inmuebles.objects.create(
        pk_estado_fisico_predio=estado_fisico,
        tipo_predio=tipo_predios,
        tenencia_predio=tenencia_predios,
        modificacion_física_construccion=modificacion_fisica,
        superficie_predio=superficie,
        municipio=municipio,
        ciudad_localidad=ciudad,
        uso_predio=uso_destino,
        fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=pk_fk_clave_catastral_id['clave_cat'])
    )
    
    models.Datos_Construccion.objects.create(
        fk_clave_catastral=models.Datos_Contribuyentes.objects.get(clave_catastral=pk_fk_clave_catastral_id['clave_cat']),
        techos=techos,
        pisos=pisos,
        muros=muros,
        tipo_baños=tipo_baños,
        instalacion_electrica=instalacion_electrica,
        puertas_ventanas=puertas_ventanas,
        edad=edad_años,
        niveles=niveles,
        plano_croquis = plan_croq,
        doc_just_prop = doc_just,
        ult_rec_imp = ult_rec,




        lic_obr_dem = lic_obr
    )
    
    crear_reporte_DC017(pk_fk_clave_catastral_id)

    return redirect('catastro:perfil_su_cat')
 
def crear_reporte_DC017(d_clave_cat_i):

    num_int_c =''
    num_ext_c=''
    c_c = ''
    rfc = ''
    tramite = ''
    nombre = ''
    ap = ''
    am = ''
    telefono = ''
    tipo_tel = ''
    calle = ''
    col_fracc_c = ''
    query = models.Datos_Contribuyentes.objects.filter(clave_catastral=d_clave_cat_i["clave_cat"])

    for datos_p in query:
        c_c = datos_p.clave_catastral
        rfc = datos_p.rfc
        tramite = datos_p.tramite
        nombre = datos_p.nombre
        ap = datos_p.apaterno
        am = datos_p.amaterno
        telefono = datos_p.telefono
        tipo_tel = datos_p.tipo
        calle = datos_p.calle
        num_int_c = datos_p. num_int
        num_ext_c = datos_p.num_ext
        col_fracc_c= datos_p.colonia_fraccionamiento

    num_ofi_con = functions.num_oficial(num_int_c,num_ext_c)

    datos_contribuyente = {
        "clave_catastral": c_c,
        "rfc": rfc,
        "tramite":tramite,
        "nombre": nombre,
        "ap": ap,
        "am": am,
        "telefono": telefono,
        "tipo_tel": tipo_tel,
        "calle": calle,
        "num_ofi":num_ofi_con ,
        "col_fracc": col_fracc_c
    }

    num_int_inm = ''
    col_fracc_inm = ''
    num_ext_inm = ''
    query_2 = models.Domicilio_inmueble.objects.filter(pk_fk_clave_catastral=d_clave_cat_i["clave_cat"])

    for dom_inm in query_2:
        calle = dom_inm.calle
        col_fracc_inm=dom_inm.col_fracc
        num_int_inm = dom_inm.num_int
        num_ext_inm = dom_inm.num_ext

    num_ofi_inm=functions.num_oficial(num_int_inm,num_ext_inm)

    datos_inm = {
        "calle": calle,
        "col_fracc": col_fracc_inm,
        "num_ofi": num_ofi_inm
    }



    estado_fis = ''
    tp_pred = ''
    tenen = ''
    mod_f =''
    sup = ''
    mun = ''
    ciudad = ''
    uso_d = ''
    query_3 = models.Datos_inmuebles.objects.filter(fk_clave_catastral=d_clave_cat_i["clave_cat"])

    for d_inm in query_3:
        estado_fis = d_inm.pk_estado_fisico_predio
        tp_pred = d_inm.tipo_predio
        tenen = d_inm.tenencia_predio
        mod_f = d_inm.modificacion_física_construccion
        sup = d_inm.superficie_predio
        mun = d_inm.municipio
        ciudad = d_inm.ciudad_localidad
        uso_d = d_inm.uso_predio

    detalles_inm = {
        "estado_fis": estado_fis,
        "tp_pred": tp_pred,
        "tenen": tenen,
        "mod_f": mod_f,
        "sup": sup+"m2",
        "mun": mun,
        "ciudad": ciudad,
        "uso_d": uso_d
    }

    techos = ''
    pisos  = ''
    muros  = ''
    tp_ba = ''
    inst_e = ''
    puertas_v = ''
    edad_inm= ''
    niv = ''
    plan_cro = ''
    doc_jus = ''
    ult_rec = ''
    lic_obr = ''
    dat_con= []
    query_4 = models.Datos_Construccion.objects.filter(fk_clave_catastral=d_clave_cat_i["clave_cat"])
    
    for dat_con in query_4:
        techos = dat_con.techos
        pisos = dat_con.pisos
        muros = dat_con.muros
        tp_ba = dat_con.tipo_baños
        inst_e = dat_con.instalacion_electrica
        puertas_v = dat_con.puertas_ventanas
        edad_inm=dat_con.edad
        niv = dat_con.niveles
        plan_cro = dat_con.plano_croquis
        doc_jus = dat_con.doc_just_prop
        ult_rec = dat_con.ult_rec_imp
        lic_obr = dat_con.lic_obr_dem

    c_plan_cro=functions.checkbox_rep(plan_cro)
    c_doc_jus=functions.checkbox_rep(doc_jus)
    c_ult_rec=functions.checkbox_rep(ult_rec)
    c_lic_obr=functions.checkbox_rep(lic_obr)
    
    datos_cons = {
        "techos": techos,
        "pisos": pisos,
        "muros": muros,
        "tp_ba": tp_ba,
        "inst_e": inst_e,
        "puertas_v": puertas_v,
        "edad":edad_inm,
        "niv": niv,
        "pla_cro":c_plan_cro,
        "doc_jus":c_doc_jus,
        "ult_rec":c_ult_rec,
        "lic_obr":c_lic_obr
    }

    functions.crear_reporte_p(d_clave_cat_i, datos_contribuyente, datos_inm, detalles_inm,datos_cons)


"""---FICHA CATASTRAL"""
"""--- APARTADO 1 DATOS GENERALES ---"""
#CONSULTAR DATOS GENERALES DEL CONTRIBUYENTES PARA FICHA CATASTRAL

def redirigir(request):
    return redirect('catastro:perfil_su_cat')

def obtener_datos_busqueda_ficha(request, *args,**kwargs):
    search = request.GET.get('search')
    lista = []

    if search:

        con = Domicilio_inmueble.objects.select_related().filter(Q(pk_fk_clave_catastral__clave_catastral__startswith = search) | Q(pk_fk_clave_catastral__nombre__startswith = search) 
                                                        | Q(pk_fk_clave_catastral__apaterno__startswith = search) | Q(pk_fk_clave_catastral__amaterno__startswith = search)) 
         

        for dato in con:
            lista.append({
                #datos generales
                'clave_catastral': dato.pk_fk_clave_catastral.clave_catastral,
                'nombre': dato.pk_fk_clave_catastral.nombre,
                'apaterno': dato.pk_fk_clave_catastral.apaterno,
                'amaterno': dato.pk_fk_clave_catastral.amaterno,
                'rfc':dato.pk_fk_clave_catastral.rfc,

                #domicilio del contribuyente
                'calle_con':dato.pk_fk_clave_catastral.calle,
                'int_con':dato.pk_fk_clave_catastral.num_int,
                'ext_con':dato.pk_fk_clave_catastral.num_ext,
                'codigo_postal':dato.pk_fk_clave_catastral.codigo_postal,
                'colonia_fraccionamiento_con':dato.pk_fk_clave_catastral.colonia_fraccionamiento,
                'localidad_con':dato.pk_fk_clave_catastral.localidad,


                #domicilio del predio
                'calle':dato.calle,
                'colonia':dato.col_fracc,
                'localidad':dato.localidad,
                'num_ext':dato.num_ext,
                'num_int':dato.num_int,


                
            })

        print(lista)

    return JsonResponse({
        'status': True,
        'payload':lista
    })

def consultar_datos_generales(request,clave,*args,**kwargs):

        lista_contribuyentes = []
        
        data = models.Datos_Contribuyentes.objects.filter(clave_catastral=clave)   
        print(data)
        for contribuyente in data:
            contribuyentes_datos = {}
            contribuyentes_datos['clave_catastral'] = contribuyente.clave_catastral
            contribuyentes_datos['rfc'] = contribuyente.rfc
            contribuyentes_datos['nombre'] = contribuyente.nombre
            contribuyentes_datos['apaterno'] = contribuyente.apaterno
            contribuyentes_datos['amaterno'] = contribuyente.amaterno
            contribuyentes_datos['calle'] = contribuyente.calle
            contribuyentes_datos['num_int'] = contribuyente.num_int
            contribuyentes_datos['num_ext'] = contribuyente.num_ext
            contribuyentes_datos['colonia_fraccionamiento'] = contribuyente.colonia_fraccionamiento
            contribuyentes_datos['localidad'] = contribuyente.localidad
            contribuyentes_datos['codigo_postal'] = contribuyente.codigo_postal
            lista_contribuyentes.append(contribuyentes_datos)
        print(lista_contribuyentes)
        data = json.dumps(lista_contribuyentes)
        return HttpResponse(data,'application/json')
   
@login_required(login_url="pag_login")
#vista ficha catastral
def ficha_catastral(request):
    ctx = {
        'nom_pag': 'Catastro',
        'titulo_pag': 'FICHA CATASTRAL',
    }
    return render(request,'catastro/ficha_catastral.html', ctx)

def registrar_ficha_datosgenerales(request):
   
   

    clave_catastral = request.POST['busqueda']
    d_clave_cat = {    
        "clave_cat": clave_catastral
    }

    #atributos para registrar datos del documento
    lugar_expedision = request.POST['lugar_expedision']
    td = request.POST['td']
    num_documento = request.POST['no_documento']
    dia = request.POST['predio_dia']
    mes = request.POST['predio_mes']
    año = request.POST['predio_año']
    num_notaria = request.POST['notaria']

    #atributos para registrar datos del predio
    tipo_avaluo = request.POST['tipo_avaluo']
    fraccionamiento = request.POST['fracc_']
    traslado_dominio = request.POST['tras_dominio']
    regimen = request.POST['regimen_legal']
    tenencia = request.POST['tenencia_pred']
    estado_fisico = request.POST['est_fisico']
    codigo_uso = request.POST['cod_uso']
    tipo_posecion = request.POST['tipo_posesion']
    num_emision = request.POST['no_emision']
    tipo_predio = request.POST['f_tipopredio']
    uso_predio = request.POST['f_uso_predio']

    #atributos para registrar datos de inscripcion del predio 
    tipo = 'ACTUAL'
    bajo_numero = request.POST['bajo_numero']
    tomo = request.POST['tomo']
    dia_i = request.POST['dia_inscripcion']
    mes_i = request.POST['mes_inscripcion']
    año_i = request.POST['año_inscripcion']
    zona_i = request.POST['zona_inscripcion']

    tipo_2= 'ANTECEDENTE'
    bajo_numero_2 = request.POST['bajo_numero_2']
    tomo_2 = request.POST['tomo_2']
    dia_inscripcion_2 = request.POST['dia_inscripcion_2']
    mes_inscripcion_2 = request.POST['mes_inscripcion_2']
    año_inscripcion_2 = request.POST['año_inscripcion_2']
    zona_inscripcion_2 = request.POST['zona_inscripcion_2']

    models.datos_documento_predio.objects.create(
       pk_clave_catastral=clave_catastral,
       lugar_expedision = lugar_expedision,
       td = td,
       num_documento = num_documento,
       dia = dia,
       mes = mes,
       año = año,
       num_notaria = num_notaria
    )

    models.datos_predio_ficha.objects.create(
       pk_clave_catastral=clave_catastral,
       tipo_avaluo = tipo_avaluo,
       fraccionamiento =fraccionamiento,
       traslado_dominio = traslado_dominio,
       regimen = regimen,
       tenencia = tenencia,
       estado_fisico = estado_fisico,
       codigo_uso = codigo_uso,
       tipo_posecion = tipo_posecion,
       num_emision = num_emision,
       tipo_predio = tipo_predio,
       uso_predio = uso_predio,
    )

    models.datos_inscripcion.objects.create(
     pk_fk_clave_catastral = clave_catastral,
     tipo = tipo,
     bajo_numero = bajo_numero,
     tomo = tomo,
     dia_i = dia_i,
     mes_i = mes_i,
     año_i = año_i,
     zona_i = zona_i
    )

    models.datos_inscripcion.objects.create(
     pk_fk_clave_catastral = clave_catastral,
     tipo = tipo_2,
     bajo_numero = bajo_numero_2,
     tomo = tomo_2,
     dia_i = dia_inscripcion_2,
     mes_i = mes_inscripcion_2,
     año_i = año_inscripcion_2,
     zona_i = zona_inscripcion_2
    )


    return registrar_ficha_terrenos_rurales(request) 

#ALMACENAMIENTO DE LA INFORMACIÓN DE FICHA CATASTRAL DATOS DE TERRENOS RURALES
def registrar_ficha_terrenos_rurales(request, *args,**kwargs):

    if request.GET:
       clave_catastral = request.GET.get("clave_catatastral_id")
       t_suelo = request.GET.get("t_suelo")
       valor_has = request.GET.get("valor_has")
       sup_has = request.GET.get("has")
       a = request.GET.get("a")
       c = request.GET.get("c")
       top = request.GET.get("top")
       vias_c = request.GET.get("vias_c")

       models.terrenos_rurales.objects.create(
           pk_fk_clave_catastral = clave_catastral,
           tipo_suelo = t_suelo,
           valor_has = valor_has,
           sup_has=sup_has,
           a=a,
           c=c,
           top=top,
           vias_c=vias_c
       )
       print("rurales ok")
       return HttpResponse("DATOS DE TERRENOS RURALES OK")
    return HttpResponse("metodo no permitido")

#ALMACENAMIENTO DE LA INFORMACIÓN DE FICHA CATASTRAL DATOS DE TERRENOS RURALES (superficie total)
def registrar_ficha_terrenos_rurales_supertotal(request, *args,**kwargs):

    if request.GET:
        clave_catastral = request.GET.get("clave_catatastral_id")
        has_st = request.GET.get("has_st")
        a_st = request.GET.get("a_st")
        c_st = request.GET.get("c_st")

        models.terrenos_rurales_superficietotal.objects.create(
            pk_fk_clave_catastral = clave_catastral,
            sup_t_has = has_st,
            a = a_st,
            c = c_st
        )
        print("rurales total super ok")
        return HttpResponse("SUPER TOTAL OK")
    return HttpResponse("metodo no permitido")

#ALMACENA LA INFORMACIÓN DE FICHA CATASTRAL DE DATOS DE TERRENOS URBANOS (GENERAL)
def registrar_ficha_terrenos_urbanos(request, *args,**kwargs):

    if request.GET:
        clave_catastral = request.GET.get("clave_catastral_tu")
        valor2_m2 = request.GET.get("valor2_m2")
        area_terreno = request.GET.get("area_terreno")
        c_s = request.GET.get("c_s")
        valor_m2 = request.GET.get("valor_m2")
        frente = request.GET.get("frente")
        profundidad = request.GET.get("profundidad")

        models.terrenos_urbanos_suburbanos.objects.create(
           fk_clave_catastral = clave_catastral,
           valor_m2 =valor2_m2,
           area = area_terreno,
           c = c_s,
           frente = frente,
           profundidad = profundidad,
           valor = valor_m2,
        )
        print("urbanos ok")
        return HttpResponse("TERRENOS URBANOS OK")
    return HttpResponse("metodo no permitido")

#ALMACENA LA INFORMACIÓN DE FICHA CATASTRAL DE DATOS DE TERRENOS URBANOS (INCREMENTOS)
def registrar_ficha_terrenos_urbanos_incremento(request, *args,**kwargs):
    if request.GET:
        clave_catastral = request.GET.get("clave_catastral_tu")
        tipo_in = request.GET.get("tipo_in")
        valor_in = request.GET.get("valor_in")

        models.incrementos_esquina_urbanos.objects.create(
           fk_clave_catastral = clave_catastral,
           tipo =tipo_in,
           valor = valor_in,
        )
        print("urbanos incremento ok")
        return HttpResponse("INCREMENTOS OK")
    return HttpResponse("metodo no permitido")

#ALMACENA LA INFORMACIÓN DE FICHA CATASTRAL DE DATOS DE TERRENOS URBANOS (DEMERITOS)
def registrar_ficha_terrenos_urbanos_demeritos(request, *args,**kwargs):
    if request.GET:
        clave_catastral = request.GET.get("clave_catastral_tu")
        descripcion_de = request.GET.get("descripcion_de")
        valor_de = request.GET.get("valor_de")

        models.demeritos_predios_urbanos.objects.create(
           fk_clave_catastral = clave_catastral,
           descripcion =descripcion_de,
           valor = valor_de,
        )
        print("urbanos demeritos ok")
        return HttpResponse("DEMERITOS OK")
    return HttpResponse("metodo no permitido")

#ALMACENA LA INFORMACIÓN DE LA FICHA CATASTRAL DE DATOS DE CONSTRCCIONES DEL PREDIO
def registrar_ficha_datos_construcciones(request, *args,**kwargs):
    if request.GET:
        clave_cat = request.GET.get("clave_catastral_dc")
        etiqueta = request.GET.get("etiqueta")
        tipo_c = request.GET.get("tipo_c")
        est = request.GET.get("est")
        terreno = request.GET.get("terreno")
        antiguedad = request.GET.get("antiguedad")
        area_c = request.GET.get("area_c")

        fk_clave_cat = get_object_or_404(models.Datos_Contribuyentes, clave_catastral=clave_cat)

        models.ficha_datos_construcciones.objects.create(
            etiqueta=etiqueta,
            fk_clave_catastral = fk_clave_cat,
            tipo_c=tipo_c,
            est=est,
            terreno=terreno,
            antiguedad=antiguedad,
            area_c=area_c
           
        )
        crear_ficha_catastral(clave_cat)
        return HttpResponse("CONSTRUCCIONES OK")
    return HttpResponse("metodo no permitido")

#ALMACENA LOS VALORES MONETARIOS DEL PREDIO
def registrar_valores(request):

    #Este ultimo metodo es para poder darle guardar e imprimir el reporte
    zoncat = request.POST['fc_zon']
    mun = request.POST['fc_mu']
    loc = request.POST['fc_loc']
    reg = request.POST['fc_re']
    man = request.POST['fc_ma']
    lot = request.POST['fc_lot']
    niv = request.POST['fc_ni']
    dep = request.POST['fc_de']
    dv = request.POST['fc_dv']
    clave_catastral = zoncat + mun + loc + reg + man + lot + niv + dep + dv

    datos_clav_c = {
        "C_ZON" : zoncat,
        "C_MUN" : mun,
        "C_LOC" : loc,
        "C_REG" : reg,
        "C_MAN" : man,
        "C_LOT" : lot,
        "C_NIV" : niv,
        "C_DP" : dep,
        "C_DV" : dv,
        "clave_cat":clave_catastral
    }

    valor_te = request.POST['va_te']
    valor_co = request.POST['va_co']
    valor_cat = request.POST['va_ca']

    models.valores_catastro.objects.create(
        clave_catastral_pk = clave_catastral,
        valor_terreno = valor_te,
        valor_construccion = valor_co,
        valor_catastral = valor_cat,
    )

    
    return HttpResponseRedirect(reverse('menu_secundario'))

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

""""
def enviar(request):
    id= request.POST['id']
    
    usuario_remtitente= User.objects.get(username=request.user.username)
    usuario_destino = User.objects.get(username=id)
    cuerpo= request.POST['cuerpo']
    cuerpo2= request.POST['cuerpo2']
    
    
    notify.send(usuario_remtitente, recipient=usuario_destino, verb=cuerpo,description=cuerpo2)
    
"""
@login_required(login_url='pag_login')
def cambiar_password(request):
    username = request.POST['username']
    password = request.POST['password']
    conf_password = request.POST['conf_password']

def view_notify(request):
    return render(request,'catastro/notification_2.html')
    
def send_notify_test(request):

    remitente = request.user.username
    destinatario = request.POST['destinatario']
    id_dest = User.objects.get(username=destinatario)
    titulo = request.POST['titulo']
    cuerpo = request.POST['cuerpo']

    
    notify_models.notify.objects.create(
        remitente=remitente,
        destinatario = id_dest,
        titulo = titulo,
        cuerpo = cuerpo
    )
    
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'consumer_notifications_{destinatario}',
        {
            'type':'update_not',
            'destinatario': destinatario
        }
    )
    
    
    return HttpResponse('Notificacion enviada')


    
    
    
