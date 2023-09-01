
//Validar inputs por medio de eventos

//campos de datos de predios

//campos de la clave catastral
const zonacat = document.querySelector("[name=zonacat]")
const muni = document.querySelector("[name=muni]")
const loc = document.querySelector("[name=loc]")
const region = document.querySelector("[name=region]")
const manzana = document.querySelector("[name=manzana]")
const lote = document.querySelector("[name=lote]")
const nivel = document.querySelector("[name=nivel]")
const depto = document.querySelector("[name=depto]")
const dv = document.querySelector("[name=dvs]")


const fecha_registro = document.querySelector("[name=fecha_registro]")
const motivo_registro = document.querySelector("[name=motivo_registro]")
const cuenta_predial = document.querySelector("[name=cuenta_predial]")
const denominacion = document.querySelector("[name=denominacion]")
const cuenta_origen = document.querySelector("[name=cuenta_origen]")
const tipo_predio = document.querySelector("[name=tipo_predio]")
const uso_predio = document.querySelector("[name=uso_predio]")

const region_2 = document.querySelector("[name=region_2]")
const zona_valor = document.querySelector("[name=zona_valor]")



const municipio_predio = document.querySelector("[name=municipio_predio]")
const localidad_predio = document.querySelector("[name=localidad_predio]")
const colonia_predio = document.querySelector("[name=colonia_predio]")
const calle_predio = document.querySelector("[name=calle_predio]")


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

document.addEventListener("DOMContentLoaded", function() {
  // Tu código aquí

  fecha_registro.addEventListener("blur", (e) => validarCamposVacios("Ingrese la fecha de registro",e))
  motivo_registro.addEventListener("blur", (e) => validarCamposVacios("Ingrese el motivo de registro",e))
  cuenta_predial.addEventListener("blur",(e) => validarCamposVacios("Ingrese una cuenta predial",e))
  denominacion.addEventListener("blur",(e) => validarCamposVacios("Ingrese una denominación",e))
  cuenta_origen.addEventListener("blur",(e) => validarCamposVacios("Ingrese una cuenta de origen",e))
  tipo_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese el tipo de predio",e))
  uso_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese el uso del predio",e))

  region_2.addEventListener("blur", (e) => validarCamposVacios("Ingrese una región",e))
  zona_valor.addEventListener("blur", (e) => validarCamposVacios("Ingrese una zona de valor",e))

  municipio_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese un municipio",e))
  localidad_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese una localidad",e))
  colonia_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese una colonia",e))
  calle_predio.addEventListener("blur", (e) => validarCamposVacios("Ingrese una calle",e))

zonacat.addEventListener("blur", (e) => validarCamposVacios("",e))
muni.addEventListener("blur", (e) => validarCamposVacios("",e))
loc.addEventListener("blur", (e) => validarCamposVacios("",e))
region.addEventListener("blur", (e) => validarCamposVacios("",e))
manzana.addEventListener("blur", (e) => validarCamposVacios("",e))
lote.addEventListener("blur", (e) => validarCamposVacios("",e))
nivel.addEventListener("blur", (e) => validarCamposVacios("",e))
depto.addEventListener("blur", (e) => validarCamposVacios("",e))
dv.addEventListener("blur", (e) => validarCamposVacios("",e))

});



//Function para permitir solo digitos
function SoloNumeros(evt){
    
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

function Espacios(string){
  //Uso de split y join para buscar y reemplazar caracteres
  //Reemplazando espacios por guiones
  return string.split(" ").join("-");
}

//Función que permite solo letras
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


function soloLetrasNumeros(e) {
  key = e.keyCode || e.which;
  tecla = String.fromCharCode(key).toString();
  letras = "áéíóúÁÉÍÓÚabcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";//Se define todo el abecedario que se quiere que se muestre.
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