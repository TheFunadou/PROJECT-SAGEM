document.getElementById('zona_inscripcion_2')//Función para hacer un submit en el formulario y mandar los datos a la BD al pulsar enter
.addEventListener('keyup', function(event) {
    if (event.code === 'Enter'){
       event.preventDefault();
       document.querySelector('form').submit();
    }
});



var elInput = document.getElementById('fc_dv');
elInput.addEventListener('keyup', function(e) {
  var keycode = e.keyCode || e.which;
  if (keycode == 13) {

    var zona = document.getElementById('fc_zon').value
    var municipio = document.getElementById('fc_mu').value
    var localidad = document.getElementById('fc_loc').value
    var region = document.getElementById('fc_re').value
    var manzana = document.getElementById('fc_ma').value
    var lote = document.getElementById('fc_lot').value
    var nivel = document.getElementById('fc_ni').value
    var departamento = document.getElementById('fc_de').value
    var dv = document.getElementById('fc_dv').value
    console.log(zona +","+municipio+","+localidad+","+region+","+manzana
    +","+lote+","+nivel+","+departamento+","+dv)

    var clave_catastral = zona+municipio+localidad+region+manzana+lote+nivel+departamento+dv
  
  //petición ajax para extraer y mostrar datos generales
    $.ajax({
          
          
          url:'/menu_principal/menu_secundario/ficha_catastral_datos_generales/buscar_datos_generales/',
          dataType:'json',
          type:'GET',
          data: {'clave':clave_catastral},    
          success: function (response) {
              
              $("#fnombre").val(response[0].nombre);
              $("#fa_paterno").val(response[0].apaterno);
              $("#fa_materno").val(response[0].amaterno);
              $("#fcurp").val(response[0].rfc);
              $("#f_calle_notifica").val(response[0].calle);
              $("#f_int_notifica").val(response[0].num_int);
              $("#f_ext_notifica").val(response[0].num_ext);
              $("#f_colonia_fracc_notifica").val(response[0].colonia_fraccionamiento);
              $("#f_cp_notifica").val(response[0].codigo_postal);
              $("#f_ciudad_notifica").val(response[0].localidad);
            },
          error:function(error){
              console.log(error)
          }
    })
    
 

    //petición ajax para extraer y mostrar datos del domicilio del predio

    $.ajax({
            
            
      url:'/menu_principal/menu_secundario/ficha_catastral_datos_generales/buscar_domicilio_predio/',
      dataType:'json',
      type:'GET',
      data: {'clave':clave_catastral},    
      success: function (response) {
          
          $("#f_calle").val(response[0].calle);
          $("#f_int").val(response[0].num_int);
          $("#f_ext").val(response[0].num_ext);
          $("#f_col_fracc").val(response[0].col_fracc);
        },
      error:function(error){
          console.log(error)

    }
    });

  }
});



