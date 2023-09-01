

//función para suma los valores totales
function suma() {
  var checkboxes = document.querySelectorAll('.form-check-input');
  var suma = 0;

  checkboxes.forEach(function(checkbox) {
    var row = checkbox.closest('tr');
    if (checkbox.checked) {
      row.style.backgroundColor = '#E8E8E8';
      var valores = checkbox.value.split(",");
      var numero = parseFloat(valores[0]);
      suma += numero;
    }else{
      row.style.backgroundColor = '';
    }
  });

  document.getElementById('suma').textContent = suma;
  }

  
//funcion que pretende mandar los valores donde se ejecutara un descuento
function solicitar_descuento(){
    var año = null;
    var clave = null;
    var estatus = null;
    var añosSeleccionados = [];
    var checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
          var valores = checkbox.value.split(",");
    
          año = valores[1];
          clave = valores[2];
          estatus = valores[3]
          añosSeleccionados.push(año);
          //console.log("clave: " + clave + " año: "+ año + " Estatus: "+ estatus);
        }

      });

      

      $.ajax({
            type: 'GET',
            url: 'solicitar', // Reemplaza esto con la URL de tu vista en Django
            data: {
                'años': añosSeleccionados,
                'clave':clave,
                'estatus':estatus
            },
            dataType: 'json',
            success: function(response) {
                // Maneja la respuesta del servidor si es necesario
            },
            error: function(error) {
                console.error(error);
            }
      });
      console.log("clave: " + clave + " años: "+ añosSeleccionados + " Estatus: "+ estatus);
}






  