



const input = document.getElementById("dvs");
input.addEventListener("input", function() {
  
  var inputValue = input.value;
  var zonaca = document.getElementById('zonacat').value
  var mun = document.getElementById('muni').value
  var lo = document.getElementById('loc').value
  var reg= document.getElementById('region').value
  var man = document.getElementById('manzana').value
  var lot = document.getElementById('lote').value
  var niv = document.getElementById('nivel').value
  var dep = document.getElementById('depto').value
  var dvs = document.getElementById('dvs').value
  var characterCount = dvs.length;

  if (characterCount == 2){
    var clave = zonaca+mun+lo+reg+man+lot+niv+dep+inputValue

    $.ajax({
      headers: { 'X-CSRFToken': "{{csrf_token}}" },
      url: "existe_contribuyente/",
      data: {'clave':clave},//se envia el arreglo con la información
      type: "GET",
      dataType: 'json',
      success: function (response) {
       
          if(response.resultado==true){
            var message = '¡La clave catastral ' + '<strong>' + clave + '</strong>' +' ya existe! Ingrese otra clave catastral';
            $('.alert').addClass('alert alert-danger alert-dismissible fade show').html(message).fadeIn(900);
          }

          setTimeout(function() {
            $('.alert').fadeOut('slow');
          }, 4000);
      },
      error: function (jqXHR, textStatus, error) {
          console.log(error)
      },
      complete: function (xhr, status) {
          console.log("finalizado")
      }
    })

  }



});







