//campos de la clave catastral
const zonacat = document.querySelector("[name=fc_zon]")
const muni = document.querySelector("[name=fc_mu]")
const loc = document.querySelector("[name=fc_loc]")
const region = document.querySelector("[name=fc_re]")
const manzana = document.querySelector("[name=fc_ma]")
const lote = document.querySelector("[name=fc_lot]")
const nivel = document.querySelector("[name=fc_ni]")
const depto = document.querySelector("[name=fc_de]")
const dv = document.querySelector("[name=fc_dv]")

//datos documento
const lugar_expedición = document.querySelector("[name=lugar_expedision]")
const td = document.querySelector("[name=td]")
const no_documento = document.querySelector("[name=no_documento]")
const dia = document.querySelector("[name=predio_dia]")
const mes = document.querySelector("[name=predio_mes]")
const año = document.querySelector("[name=predio_año]")
const no_notaria = document.querySelector("[name=notaria]")

//datos predio
const tipo_avaluo = document.querySelector("[name=tipo_avaluo]")
const fra = document.querySelector("[name=fracc_]")
const traslado_dominio = document.querySelector("[name=tras_dominio]")
const regimen = document.querySelector("[name=regimen_legal]")
const tenencia = document.querySelector("[name=tenencia_pred]")
const estado_fisico = document.querySelector("[name=est_fisico]")
const cod_uso_predio = document.querySelector("[name=cod_uso]")
const tipo_posesión = document.querySelector("[name=tipo_posesion]")
const no_emision = document.querySelector("[name=no_emision]")

//datos inscripcion

const bajo_numero = document.querySelector("[name=bajo_numero]")
const tomo = document.querySelector("[name=tomo]")
const dia_inscripcion = document.querySelector("[name=dia_inscripcion]")
const mes_inscripcion = document.querySelector("[name=mes_inscripcion]")
const año_inscripcion = document.querySelector("[name=año_inscripcion]")
const zona_inscripcion = document.querySelector("[name=zona_inscripcion]")

const bajo_numero_2 = document.querySelector("[name=bajo_numero_2]")
const tomo_2 = document.querySelector("[name=tomo_2]")
const dia_inscripcion_2 = document.querySelector("[name=dia_inscripcion_2]")
const mes_inscripcion_2 = document.querySelector("[name=mes_inscripcion_2]")
const año_inscripcion_2 = document.querySelector("[name=año_inscripcion_2]")
const zona_inscripcion_2 = document.querySelector("[name=zona_inscripcion_2]")


const setErrors = (message, campo, isError=true)=>{
    if(isError){
      campo.classList.add("inputs")
      campo.nextElementSibling.classList.add("error")
      campo.nextElementSibling.innerText= message;
    }else{
      campo.classList.remove("inputs")
      campo.nextElementSibling.classList.remove("error")
      campo.nextElementSibling.innerText="";
    }
  }
  
  const validarCamposVacios = (message, e) =>{
    const campo = e.target;
    const campo_valor = e.target.value;
    if(campo_valor.trim().length == 0){
      setErrors(message,campo)
    }else{
      setErrors("",campo,false)
    }
  }


zonacat.addEventListener("blur", (e) => validarCamposVacios("",e))
muni.addEventListener("blur", (e) => validarCamposVacios("",e))
loc.addEventListener("blur", (e) => validarCamposVacios("",e))
region.addEventListener("blur", (e) => validarCamposVacios("",e))
manzana.addEventListener("blur", (e) => validarCamposVacios("",e))
lote.addEventListener("blur", (e) => validarCamposVacios("",e))
nivel.addEventListener("blur", (e) => validarCamposVacios("",e))
depto.addEventListener("blur", (e) => validarCamposVacios("",e))
dv.addEventListener("blur", (e) => validarCamposVacios("",e))

//datos generales
//datos documento
 lugar_expedición.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 td.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 no_documento.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 dia.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 mes.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 año.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 no_notaria.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))

//datos predio
 tipo_avaluo.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 fra.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 traslado_dominio.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 regimen.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 tenencia.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 estado_fisico.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 cod_uso_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 tipo_posesión.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))
 no_emision.addEventListener("blur", (e) => validarCamposVacios("Ingrese un valor",e))

//dato de inscripcion
 bajo_numero.addEventListener("blur", (e) => validarCamposVacios("",e))
 tomo.addEventListener("blur", (e) => validarCamposVacios("",e))
 dia_inscripcion.addEventListener("blur", (e) => validarCamposVacios("",e))
 mes_inscripcion.addEventListener("blur", (e) => validarCamposVacios("",e))
 año_inscripcion.addEventListener("blur", (e) => validarCamposVacios("",e))
 zona_inscripcion.addEventListener("blur", (e) => validarCamposVacios("",e))

 bajo_numero_2.addEventListener("blur", (e) => validarCamposVacios("",e))
 tomo_2.addEventListener("blur", (e) => validarCamposVacios("",e))
 dia_inscripcion_2.addEventListener("blur", (e) => validarCamposVacios("",e))
 mes_inscripcion_2.addEventListener("blur", (e) => validarCamposVacios("",e))
 año_inscripcion_2.addEventListener("blur", (e) => validarCamposVacios("",e))
 zona_inscripcion_2.addEventListener("blur", (e) => validarCamposVacios("",e))

function valideKey(evt){
    
    // code is the decimal ASCII representation of the pressed key.
    var code = (evt.which) ? evt.which : evt.keyCode;
    
    if(code==8) { // backspace.
      return true;
    } else if(code==32){
  
    }else if(code>=45 && code<=57) { // is a number.
      return true;
    } else{ // other keys.
      return false;
    }
}


function soloLetras(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toString();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚABCDEFGHIJKLMNÑOPQRSTUVWXYZ";//Se define todo el abecedario que se quiere que se muestre.
    especiales = [8, 37, 39, 46, 6]; //Es la validación del KeyCodes, que teclas recibe el campo de texto.
  
    tecla_especial = false
    for(var i in especiales) {
        if(key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }
  
    if(letras.indexOf(tecla) == -1 && !tecla_especial){
        return false;
      }
  }