window.onload = function(){
  console.log('holaaaaa');
  calcularSubtotal();
}


function calcularSubtotal(){
  var tabla_adeudos = document.getElementById('tabla_adeudos');
  var tbody = tabla_adeudos.querySelector('tbody');
  var filas = tbody.querySelector('tr');

  for (var i = 0; i <filas.length; i++){

    var celdas = filas[i].getElementsByTagName('td');

    console.log('IMPUESTO_PREDIAL: '+ celdas[2]);
    console.log('IMPUESTO_ADICIONAL: '+ celdas[3]);
    console.log('IMPUESTO_RECARGO: '+ celdas[4]);
    console.log('IMPUESTO_MULTA: '+ celdas[5]);
  }
}


//función para suma los valores totales
function suma() {
  var checkboxes = document.querySelectorAll('.form-check-input');
  var suma = 0;

  var tabla_adeudos = document.getElementById("tabla_adeudos");
  var filas = tabla_adeudos.getElementsByTagName("tr");

  checkboxes.forEach(function(checkbox) {
    var row = checkbox.closest('tr');
    if (checkbox.checked) {
      row.style.backgroundColor = '#E8E8E8';
      var valores = checkbox.value.split(",");
      console.log(valores);
      var numero = parseFloat(valores[0]);
      console.log(numero);
      suma += numero;
    }else{
      row.style.backgroundColor = '';
    }

  });

  document.getElementById('total').textContent = suma;
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
            // url: 'solicitar', // Reemplaza esto con la URL de tu vista en Django
            url: 'solicitar',
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









  