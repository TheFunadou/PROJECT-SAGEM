const tipopredio = document.querySelector("[name=tipopredio]")
const tenenciapredio = document.querySelector("[name=tenenciapredio]")
const estadofisico = document.querySelector("[name=estadofisico]")
const modificacion = document.querySelector("[name=modificacion]")
const superficie = document.querySelector("[name=superficie]")
const municipio2 = document.querySelector("[name=municipio2]")
const ciudad2 = document.querySelector("[name=ciudad2]")
const uso = document.querySelector("[name=uso]")
const techos = document.querySelector("[name=techos]")
const pisos = document.querySelector("[name=pisos]")
const muros = document.querySelector("[name=muros]")
const tipobaño = document.querySelector("[name=tipobaño]")
const instalacionelectrica = document.querySelector("[name=instalacionelectrica]")
const puertaventana = document.querySelector("[name=puertaventana]")
const años = document.querySelector("[name=años]")
const niveles = document.querySelector("[name=niveles]")

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

  tipopredio.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de predio",e))
  tenenciapredio.addEventListener("blur",(e) => validarCamposVacios("Seleccione la tenencia del predio",e))
  estadofisico.addEventListener("blur",(e) => validarCamposVacios("Seleccione el estado físico",e))
  modificacion.addEventListener("blur",(e) => validarCamposVacios("Seleccione la modificación",e))
  superficie.addEventListener("blur",(e) => validarCamposVacios("Ingrese la superficie",e))
  municipio2.addEventListener("blur",(e) => validarCamposVacios("Ingrese el municipio",e))
  ciudad2.addEventListener("blur",(e) => validarCamposVacios("Ingrese la ciudad o localidad",e))
  uso.addEventListener("blur",(e) => validarCamposVacios("Seleccione le uso del predio",e))
  techos.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de techo",e))
  pisos.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de piso",e))
  muros.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de muro",e))
  tipobaño.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de baño",e))
  instalacionelectrica.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de instalación eléctrica",e))
  puertaventana.addEventListener("blur",(e) => validarCamposVacios("Seleccione el tipo de puerta",e))
  años.addEventListener("blur",(e) => validarCamposVacios("Ingrese los años",e))
  niveles.addEventListener("blur",(e) => validarCamposVacios("Ingrese el número de niveles",e))


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