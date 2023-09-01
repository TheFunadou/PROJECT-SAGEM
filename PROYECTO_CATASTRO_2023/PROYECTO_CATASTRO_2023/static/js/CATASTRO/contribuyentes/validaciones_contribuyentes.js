
//Validar inputs por medio de eventos

//campos de datos de contribuyentes


const num_identificacion = document.querySelector("[name=num_identificacion]")
const nombre = document.querySelector("[name=nombre_razon]")
const apaterno = document.querySelector("[name=apaterno]")
const amaterno = document.querySelector("[name=amaterno]")
const rfc = document.querySelector("[name=rfc]")
const curp = document.querySelector("[name=curp]")

const fecha_nacimiento = document.querySelector("[name=fecha_nacimiento]")



const munic = document.querySelector("[name=munic]")
const localidad = document.querySelector("[name=loca]")
const colon = document.querySelector("[name=colon]")
const cp = document.querySelector("[name=cp]")
const calle = document.querySelector("[name=calle]")






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

  num_identificacion.addEventListener("blur", (e) => validarCamposVacios("Ingresa el No. de identificación",e))
  apaterno.addEventListener("blur", (e) => validarCamposVacios("Ingresa un apellido peterno",e))
  amaterno.addEventListener("blur",(e) => validarCamposVacios("Ingresa un apellido materno",e))
  nombre.addEventListener("blur",(e) => validarCamposVacios("Ingresa un nombre",e))
  rfc.addEventListener("blur",(e) => validarCamposVacios("Ingresa un RFC",e))
  curp.addEventListener("blur", (e) => validarCamposVacios("Ingresa una CURP",e))
  fecha_nacimiento.addEventListener("blur", (e) => validarCamposVacios("Ingresa una fecha",e))

  munic.addEventListener("blur", (e) => validarCamposVacios("Ingresa un municipio",e))
  localidad.addEventListener("blur", (e) => validarCamposVacios("Ingresa una localidad",e))
  colon.addEventListener("blur", (e) => validarCamposVacios("Elige una colonia",e))
  cp.addEventListener("blur", (e) => validarCamposVacios("Ingresa un código postal",e))
  calle.addEventListener("blur", (e) => validarCamposVacios("Ingresa una calle",e))

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