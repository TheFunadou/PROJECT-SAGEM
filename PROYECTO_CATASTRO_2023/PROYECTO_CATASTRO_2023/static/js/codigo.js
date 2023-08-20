
   function ocultar(e) {//Función para habilitar y deshabilitar un div

    if (e.code === "Enter") {
        e.preventDefault();
        document.getElementById("1").style.display="none";
        document.getElementById("2").style.display="";
      }

   }

   
document.getElementById('dv')//Función para hacer un submit en el formulario y mandar los datos a la BD al pulsar enter
.addEventListener('keyup', function(event) {
    if (event.code === 'Enter'){
       event.preventDefault();
       document.querySelector('form').submit();
    }
});