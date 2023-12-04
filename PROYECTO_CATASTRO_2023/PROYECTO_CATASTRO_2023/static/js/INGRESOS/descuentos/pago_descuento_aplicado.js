window.onload = function () {
    suma()

};


// function suma() {

//     var suma_subtotal = 0;
//     var suma_multa = 0;
//     var suma_recargo = 0;
//     var suma_impuesto = 0;
//     var checkboxes = document.querySelectorAll('.form-check-input');
//     var valores = '';
//     var tabla = document.getElementById('tabla_adeudos_predial');

//     checkboxes.forEach(function (checkbox) {


//         var row = checkbox.closest('tr');
//         if (checkbox.checked) {
//             row.style.backgroundColor = '#E8E8E8';
//             var valores = checkbox.value.split(",");
//             var subtotal = parseFloat(valores[1])
//             var multa = parseFloat(valores[2]);
//             var recargo = parseFloat(valores[3]);
//             var impuesto = parseFloat(valores[4]);

//             suma_subtotal = suma_subtotal + subtotal;
//             suma_multa = suma_multa + multa;
//             suma_recargo = suma_recargo + recargo;
//             suma_impuesto = suma_impuesto + impuesto;


//         } else {

//             row.style.backgroundColor = '';

//         }

//     });

//     document.getElementById('subtotal').textContent = suma_subtotal.toFixed(2);
//     //document.getElementById('multa').textContent = suma_multa;
//     //document.getElementById('recargo').textContent = suma_recargo;
//     document.getElementById('impuesto_adicional').textContent = suma_impuesto;

//     //let valor_recargo = document.getElementById('recargo').textContent;
//     //let valor_multa = document.getElementById('multa').textContent;

//     let v_desc_recargo = '0.' + document.getElementById('desc_recargo').textContent;
//     let v_desc_multa = '0.' + document.getElementById('desc_multa').textContent;

//     let desc_recargo = parseFloat(valor_recargo) * parseFloat(v_desc_recargo);
//     let desc_multa = parseFloat(valor_multa) * parseFloat(v_desc_multa);

//     //document.getElementById('recargo').textContent = desc_recargo;
//     //valor_multa = document.getElementById('multa').textContent = desc_multa;


// }

