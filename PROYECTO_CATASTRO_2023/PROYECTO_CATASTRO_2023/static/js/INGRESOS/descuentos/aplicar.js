window.onload = function() {
    suma() 
};


function suma() {

    var checkboxes = document.querySelectorAll('.form-check-input');
    var suma_total = 0;
    var multa_total = 0;
    var recargo_total = 0;
    var suma_impuesto = 0;
    var suma_subtotal =0;
    var valores = '';
    
    checkboxes.forEach(function(checkbox) {
      

      var row = checkbox.closest('tr');
      if (checkbox.checked) {  
        row.style.backgroundColor = '#E8E8E8';
        var valores = checkbox.value.split(",");
        var total = parseFloat(valores[0]);
        var subttotal = parseFloat(valores[1])
        var multa = parseFloat(valores[2]);
        var recargo = parseFloat(valores[3]);
        var impuesto_adicional = parseFloat(valores[4]);

        suma_total += total;
        multa_total += multa;
        recargo_total += recargo
        suma_impuesto += impuesto_adicional
        suma_subtotal += subttotal
  
      }else{
        
        row.style.backgroundColor = '';
  
      }
 
    });

    document.getElementById('suma_total').textContent = suma_total;
    document.getElementById('multa').textContent = multa_total;
    document.getElementById('recargo').textContent = recargo_total;
    document.getElementById('impuesto_adicional').textContent = suma_impuesto;
    document.getElementById('subtotal').textContent = suma_subtotal.toFixed(2); 
    
    
}


function descuento_multa(){

    var checkboxes = document.querySelectorAll('.form-check-input');
    var multa_total = 0;
    var porcentaje_multa =0

    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {  
          var valores = checkbox.value.split(",");
          var multa = parseFloat(valores[2]);
          multa_total += multa;
          
        }
        
  });

    porcentaje_multa = document.getElementById('multas').value
    var descuento_multa = (porcentaje_multa/100)*multa_total;
    var resultado_multa_desc = multa_total - descuento_multa;
    var span_multa = document.getElementById('multa')

    span_multa.textContent = resultado_multa_desc.toFixed(2);

    if(porcentaje_multa.length > 0){
      span_multa.style.color = 'red';
    }else if(porcentaje_multa.length == 0){
      span_multa.style.color = '#25758d';
    }

    suma_total_descuento()
   

}   


function descuento_recargo(){

  var checkboxes = document.querySelectorAll('.form-check-input');
  var recargo_total = 0;
  var porcentaje_recargo=0

  checkboxes.forEach(function(checkbox) {
      if (checkbox.checked) {  
        var valores = checkbox.value.split(",");    
        var recargo = parseFloat(valores[3]);
        recargo_total += recargo
        
      }
      
});

  porcentaje_recargo = document.getElementById('recargos').value
  var descuento_recargo = (porcentaje_recargo/100)*recargo_total;
  var resultado_recargo_desc = recargo_total - descuento_recargo;

  var span_recargo = document.getElementById('recargo')
  span_recargo.style.color = 'red';
  span_recargo.textContent = resultado_recargo_desc.toFixed(2);

  if(porcentaje_recargo.length > 0){
    span_recargo.style.color = 'red';
  }else if(porcentaje_recargo.length == 0){
    span_recargo.style.color = '#25758d';
  }

  suma_total_descuento()

 
}   

function suma_total_descuento(){
  var resultado_total = 0
  var subtotal_total =0
  var impuesto_adicional_total=0
  var recargo_total=0
  var multa_total=0;

  subtotal_total = parseFloat(document.getElementById('subtotal').textContent) 
  impuesto_adicional_total =  parseFloat(document.getElementById('impuesto_adicional').textContent) 
  recargo_total = parseFloat(document.getElementById('recargo').textContent) 
  multa_total = parseFloat(document.getElementById('multa').textContent) 


  resultado_total = subtotal_total+impuesto_adicional_total + recargo_total + multa_total;
  var input = document.getElementById("total_descuento");
  input.value = resultado_total.toFixed(2);

}


//funcion que pretende mandar los valores donde se ejecutara un descuento
function aplicar_descuento(){
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

    console.log('dddddd')

    $.ajax({
          type: 'GET',
          url: '/descuento_aplicado', // Reemplaza esto con la URL de tu vista en Django
          data: {
             
              'clave':clave,
              
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




