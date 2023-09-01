function realizarSolicitudAJAX() {
    // Aquí colocas tu código para realizar la solicitud AJAX
    // Por ejemplo, usando jQuery:
    $.ajax({
      url: 'xd/',
      method: 'GET',
      success: function(data) {
        var cantidadElementos = data.cantidad_elementos;
        // Actualiza el contenido del span con la cantidad de elementos
        document.getElementById("box_num_notify").textContent = cantidadElementos;
      },
      error: function(error) {
        // Manejar errores si es necesario
      }
    });
  }
  
  // Establecer un temporizador para ejecutar la solicitud AJAX cada 1 minuto (60,000 milisegundos)
  setInterval(realizarSolicitudAJAX, 1000);