
window.onload = function () {
    calcularSubtotal();
    suma();
    recargo();
    multa();
    calcularDescuento();
}


function calcularSubtotal() {
    var tabla_adeudos = document.getElementById('tabla_adeudos');
    var tbody = tabla_adeudos.querySelector('tbody');
    var filas = tbody.getElementsByTagName('tr');

    for (var i = 0; i < filas.length; i++) {

        var celdas = filas[i].getElementsByTagName('td');

        subtotal = parseFloat(celdas[2].textContent) + parseFloat(celdas[3].textContent) + parseFloat(celdas[4].textContent) + parseFloat(celdas[5].textContent);

        // INSERTAR EL LA COLUMA SUBTOTAL EL VALOR DE LA SUMA
        celdas[6].innerHTML = subtotal.toFixed(2);

    }
}

//función para suma los valores totales
function suma() {
    var checkboxes = document.querySelectorAll('.form-check-input');
    var input_total = document.getElementById('total');

    var celda_impuesto_pred = document.getElementById('sum_impuesto_pred');
    var celda_impuesto_adic = document.getElementById('sum_impuesto_adic');
    var celda_recargo = document.getElementById('sum_recargo');
    var celda_multa = document.getElementById('sum_multa');
    var celda_subtotal = document.getElementById('sum_subtotal');

    var sum_impuesto_pred = 0;
    var sum_impuesto_adi = 0;
    var sum_recargo = 0;
    var sum_multa = 0;
    var sum_subtotal = 0;
    var total = 0;

    checkboxes.forEach(function (checkbox) {
        var row = checkbox.closest('tr');

        // IF PARA HACER ACCIONES SI EL CHECKBOX ESTA HABILITADO
        if (checkbox.checked) {
            // CAMBIAR EL COLOR DE LA FILA SELECCIONADA
            row.style.backgroundColor = '#E8E8E8';

            var celdas = row.getElementsByTagName('td');
            // EXTRAER ELEMENTOS SELECCIONADOS
            var impuesto_predial = parseFloat(celdas[2].textContent);
            var impuesto_adicional = parseFloat(celdas[3].textContent);
            var recargo = parseFloat(celdas[4].textContent);
            var multa = parseFloat(celdas[5].textContent);
            var subtotal = parseFloat(celdas[6].textContent);


            // SUMAR COLUMNAS
            sum_impuesto_pred += impuesto_predial;
            sum_impuesto_adi += impuesto_adicional;
            sum_recargo += recargo;
            sum_multa += multa;
            sum_subtotal += subtotal;
            // Calcular total sumando subtotal
            total += subtotal;

            // INSERTAR SUMA DEL TOTAL SELECCIONADO EN EL INPUT
            celda_impuesto_pred.textContent = sum_impuesto_pred.toFixed(2);
            celda_impuesto_adic.textContent = sum_impuesto_adi.toFixed(2);
            celda_recargo.textContent = sum_recargo.toFixed(2);
            celda_multa.textContent = sum_multa.toFixed(2);
            celda_subtotal.textContent = sum_subtotal.toFixed(2);
            input_total.value = total.toFixed(2);

        } else {
            row.style.backgroundColor = '';
        }

    });

    // Verificar si no se seleccionaron checkboxes y establecer el valor en 0.00
    if (total == 0) {
        celda_impuesto_pred.textContent = '0.00';
        celda_impuesto_adic.textContent = '0.00';
        celda_recargo.textContent = '0.00';
        celda_multa.textContent = '0.00';
        celda_subtotal.textContent = '0.00';
        input_total.value = '0.00';
    }
}

function recargo(){
    var celda_recargo = document.getElementById('sum_recargo');
    var celda_desc_recargo = document.getElementById('desc_recargo');
    var select_recargo = parseFloat(document.getElementById('select_recargo').value);
    console.log('valor recargo:' + select_recargo);
   
    var calc_descuento  = parseFloat(celda_recargo.textContent.trim()) * select_recargo;
    console.log(calc_descuento);
    celda_desc_recargo.textContent = calc_descuento.toFixed(2);

    calcularDescuento();

}

function multa(){
    var celda_multa = document.getElementById('sum_multa');
    var celda_desc_multa = document.getElementById('desc_multa');
    var select_multa = parseFloat(document.getElementById('select_multa').value);
    console.log('valor multa:' + select_multa);

    var calc_descuento  = parseFloat(celda_multa.textContent.trim()) * select_multa;
    console.log(calc_descuento);
    celda_desc_multa.textContent = calc_descuento.toFixed(2);

    calcularDescuento();
}


function calcularDescuento(){
    var celda_desc_recargo = document.getElementById('desc_recargo');
    var celda_desc_multa = document.getElementById('desc_multa');
    var input_total_desc = document.getElementById('total_descuento');
    var celda_subtotal = document.getElementById('sum_subtotal');
    var input_total = document.getElementById('total');

    var calc_desc_total = parseFloat(celda_desc_recargo.textContent.trim()) + parseFloat(celda_desc_multa.textContent.trim());
    input_total_desc.value = calc_desc_total.toFixed(2);

    var calc_total = parseFloat(celda_subtotal.textContent.trim()) - calc_desc_total;
    input_total.value = calc_total.toFixed(2);

}
