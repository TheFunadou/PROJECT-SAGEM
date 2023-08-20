
//Validar inputs por medio de eventos

//campos de datos de contribuyentes
const apaterno = document.querySelector("[name=apaterno]")
const amaterno = document.querySelector("[name=amaterno]")
const nombre = document.querySelector("[name=nombre]")
const rfc = document.querySelector("[name=rfc]")
const telefono = document.querySelector("[name=telefono]")
const tipo = document.querySelector("[name=tipo]")
const calle = document.querySelector("[name=calle]")
const colonia_fraccionamiento = document.querySelector("[name=colonia_fraccionamiento]")
const localidad = document.querySelector("[name=localidad]")
const codigo_postal = document.querySelector("[name=codigo_postal]")
//campos datos del inmuble
const calle2 = document.querySelector("[name=calle2]")
const col_fracc = document.querySelector("[name=col_fracc]")
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

//validaciones de campos contribuyentes
apaterno.addEventListener("blur", (e) => validarCamposVacios("Agrega tu apellido peterno",e))
amaterno.addEventListener("blur",(e) => validarCamposVacios("Agrega tu apellido materno",e))
nombre.addEventListener("blur",(e) => validarCamposVacios("Agrega tu nombre",e))
rfc.addEventListener("blur",(e) => validarCamposVacios("Agrega tu RFC",e))
telefono.addEventListener("blur",(e) => validarCamposVacios("Agrega tu teléfono",e))
//tipo.addEventListener("blur",(e) => validarCamposVacios("Selecciona el tipo",e))
calle.addEventListener("blur",(e) => validarCamposVacios("Ingresa tu calle",e))
colonia_fraccionamiento.addEventListener("blur",(e) => validarCamposVacios("Agrega tu colonia o fraccionamiento",e))
localidad.addEventListener("blur",(e) => validarCamposVacios("Agrega tu localidad",e))
codigo_postal.addEventListener("blur",(e) => validarCamposVacios("Agrega el código postal",e))
//validaciones campos datos inmuebles
calle2.addEventListener("blur", (e) => validarCamposVacios("Ingresa la calle",e))
col_fracc.addEventListener("blur",(e) => validarCamposVacios("Ingresa tu colonia o fraccionamiento",e))
//validaciones clave catastral
zonacat.addEventListener("blur", (e) => validarCamposVacios("",e))
muni.addEventListener("blur", (e) => validarCamposVacios("",e))
loc.addEventListener("blur", (e) => validarCamposVacios("",e))
region.addEventListener("blur", (e) => validarCamposVacios("",e))
manzana.addEventListener("blur", (e) => validarCamposVacios("",e))
lote.addEventListener("blur", (e) => validarCamposVacios("",e))
nivel.addEventListener("blur", (e) => validarCamposVacios("",e))
depto.addEventListener("blur", (e) => validarCamposVacios("",e))
dv.addEventListener("blur", (e) => validarCamposVacios("",e))



//Function para permitir solo digitos
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