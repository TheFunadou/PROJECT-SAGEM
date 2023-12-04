
window.onload = function () {
    //calcularSubtotal();
    suma();
}

function strToNum(num){
    let str_num = num.replace(/[$,]/g,'');
    return parseFloat(str_num);
}

function formatNumber(num){
    var number = num.toLocaleString('es-US', { style: 'currency', currency: 'USD' })
    return number
}

function calcularSubtotal() {
    var tabla_adeudos = document.getElementById('tabla_adeudos');
    var tbody = tabla_adeudos.querySelector('tbody');
    var filas = tbody.getElementsByTagName('tr');

    for (var i = 0; i < filas.length; i++) {

        var celdas = filas[i].getElementsByTagName('td');

        subtotal = strToNum(celdas[2].textContent) + strToNum(celdas[3].textContent) + strToNum(celdas[4].textContent) + strToNum(celdas[5].textContent);

        // INSERTAR EL LA COLUMA SUBTOTAL EL VALOR DE LA SUMA
        celdas[6].innerHTML = formatNumber(subtotal);

    }

    // suma valores totales
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

    suma();
}

//función para suma los valores totales
function suma() {
    var checkboxes = document.querySelectorAll('.form-check-input');
    var input_total = document.getElementById('total');
    var input_total_sd = document.getElementById('total_sd');
    var descuento_aprobado = document.getElementById('total_descuento');
    var celda_impuesto_pred = document.getElementById('sum_impuesto_pred');
    var celda_impuesto_adic = document.getElementById('sum_impuesto_adic');
    var celda_recargo = document.getElementById('sum_recargo');
    var celda_multa = document.getElementById('sum_multa');
    // var celda_subtotal = document.getElementById('sum_subtotal');
    // var total_descuento = document.getElementById('total_descuento').value;
    // var total_anterior = document.getElementById('total_anterior');

    var sum_impuesto_pred = 0;
    var sum_impuesto_adi = 0;
    var sum_recargo = 0;
    var sum_multa = 0;
    // var sum_subtotal = 0;
    // var total = 0;

    checkboxes.forEach(function (checkbox) {
        var row = checkbox.closest('tr');

        // IF PARA HACER ACCIONES SI EL CHECKBOX ESTA HABILITADO
        if (checkbox.checked) {
            // CAMBIAR EL COLOR DE LA FILA SELECCIONADA
            row.style.backgroundColor = '#E8E8E8';

            var celdas = row.getElementsByTagName('td');
            // EXTRAER ELEMENTOS SELECCIONADOS
            var impuesto_predial = strToNum(celdas[2].textContent);
            var impuesto_adicional = strToNum(celdas[3].textContent);
            var recargo = strToNum(celdas[4].textContent);
            var multa = strToNum(celdas[5].textContent);
            // var subtotal = parseFloat(celdas[6].textContent);


            // SUMAR COLUMNAS
            sum_impuesto_pred += impuesto_predial;
            sum_impuesto_adi += impuesto_adicional;
            sum_recargo += recargo;
            sum_multa += multa;
            // sum_subtotal += subtotal;
            // Calcular total sumando subtotal
            // total += subtotal;

            // INSERTAR SUMA DEL TOTAL SELECCIONADO EN EL INPUT
            celda_impuesto_pred.textContent = formatNumber(sum_impuesto_pred);
            celda_impuesto_adic.textContent = formatNumber(sum_impuesto_adi);
            celda_recargo.textContent = formatNumber(sum_recargo);
            celda_multa.textContent = formatNumber(sum_multa);
            var total_c_desc = (strToNum(input_total_sd.value) - strToNum(descuento_aprobado.value));
            input_total.value = formatNumber(total_c_desc);

        } else {
            row.style.backgroundColor = '';
        }

    });

    // Verificar si no se seleccionaron checkboxes y establecer el valor en 0.00
    if (total == 0) {
        celda_impuesto_pred.textContent = '$0.00';
        celda_impuesto_adic.textContent = '$0.00';
        celda_recargo.textContent = '$0.00';
        celda_multa.textContent = '$0.00';
        // celda_subtotal.textContent = '0.00';
        // input_total.value = '0.00';
    }

    // total_anterior.value = (parseFloat(total_descuento) + sum_subtotal).toFixed(2);

}
