
//Agregarción de filas para la tabla de terrenos rurales
$('#c_11').keyup(function (e) {
    if (e.which == 13) {
        var t_suelo = $("#t_suelo").val();
        var valor_has = $("#valor_has").val();
        var has = $("#has").val();
        var a = $("#a").val();
        var c = $("#c_11").val();

        

        var html = `<tr><td contenteditable>${t_suelo}</td><td contenteditable>${valor_has}</td><td contenteditable>${has}</td><td contenteditable>${a}</td><td contenteditable>${c}</td></tr>`

        if (t_suelo.trim() === "" && valor_has.trim() === "" && has.trim() === "" && a.trim() === "" && c.trim() === "") {
            alert("datos vacios")
            $("#t_suelo").focus()
        } else {
           
            $("#tabla1 tbody").append(html)
        }
    }
})

$("#agregar_fila").click(function () {
    var t_suelo = $("#t_suelo").val();
    var valor_has = $("#valor_has").val();
    var has = $("#has").val();
    var a = $("#a").val();
    var c = $("#c").val();

    var html = `<tr><td contenteditable>${t_suelo}</td><td contenteditable>${valor_has}</td><td contenteditable>${has}</td><td contenteditable>${a}</td><td contenteditable>${c}</td></tr>`

    if (t_suelo.trim() === "" && valor_has.trim() === "" && has.trim() === "" && a.trim() === "" && c.trim() === "") {
        alert("datos vacios")
        $("#t_suelo").focus()
    } else {
        $("#tabla1 tbody").append(html)
    }
})

//Agregación de filas para la tabla de terrenos urbanos
$('#profundidad').keyup(function (e) {
    if (e.which == 13) {

        var valor2_m2 = $("#valor2_m2").val();
        var area_terreno = $("#area_terreno").val();
        var c_s = $("#c_s").val();
        var valor_m2 = $("#valor_m2").val();
        var frente = $("#frente").val();
        var profundidad = $("#profundidad").val();

        var html = `<tr><td contenteditable>${c_s}</td><td contenteditable>${valor_m2}</td><td contenteditable>${frente}</td><td contenteditable>${profundidad}</td></tr>`

        if (c_s.trim() === "" && valor_m2.trim() === "" && frente.trim() === "" && profundidad.trim() === "") {
            alert("datos vacios")

        } else {
            $("#tabla tbody").append(html)
        }


    }
});

//Agregar información a la tabla de datos de construcciones
$('#area_c').keyup(function (e) {
    if (e.which == 13) {

        var etiqueta = $("#etiqueta").val();
        var tipo_c = $("#tipo_c").val();
        var est = $("#est").val();
        var terreno = $("#terreno").val();
        var antiguedad = $("#antiguedad").val();
        var area_c = $("#area_c").val();


        var html = `<tr><td contenteditable>${etiqueta}</td><td contenteditable>${tipo_c}</td><td contenteditable>${est}</td><td contenteditable>${terreno}</td><td contenteditable>${antiguedad}</td><td contenteditable>${area_c}</td></tr>`

        if (etiqueta.trim() === "" && tipo_c.trim() === "" && est.trim() === "" && terreno.trim() === "" && antiguedad.trim() === "" && area_c.trim() === "") {
            alert("datos vacios")

        } else {
            $("#tabla_construccion tbody").append(html)
        }
    }
});


////Parte de codigo para ocultar y hacer visible un contenedor mediante la seleccion de un select
const selector = document.getElementById('tipo_terreno');
const div_terreno_rural = document.getElementById('terreno_rural');
const div_terreno_urbano = document.getElementById('terreno_urbano');


document.addEventListener('DOMContentLoaded', function() {
    // Tu código aquí, por ejemplo:
    selector.addEventListener('change', function() {
    div_terreno_rural.classList.add('hidden');
    div_terreno_urbano.classList.add('hidden');


    const selectedOption = selector.value;
    if (selectedOption === 'DATOS TERRENOS RURALES') {
        div_terreno_rural.classList.remove('hidden');
    } else if (selectedOption === 'DATOS DE TERRENOS URBANOS Y SUBURBANOS') {
        div_terreno_urbano.classList.remove('hidden');
    }});
    
    
});

//dependiendo que contenedor esté habilitado se hace el guardadon de la información
function validar_divs(){
    if (div_terreno_rural.classList.contains('hidden')) {
        console.log('El div de terreno rural está oculto');
        guardar_datosUrbanos();
        guardar_datosConstruccion();
    }
    if (div_terreno_urbano.classList.contains('hidden')) {
        console.log('El div de terreno urbano está oculto');
        guardar_datosRurales();
        guardar_datosConstruccion();
    }
}

//Guarda información para terrenos rurales
function guardar_datosRurales() {
    var t_suelo = $("#t_suelo").val();
    var valor_has = $("#valor_has").val();
    var has = $("#has").val();
    var a = $("#a").val();
    var c = $("#c").val();

    var top = $("#top").val();
    var vias_c = $("#vias_c").val();

    var has_st = $("#has_st").val();
    var a_st = $("#a_st").val();
    var c_st = $("#c_st").val();


    var clave_catastral = document.getElementById('busqueda').value
   
    if (t_suelo.trim() === "" && valor_has.trim() === "" && has.trim() === "" && a.trim() === "" && c.trim() === "") {

        alert("datos vacios")
        $("#t_suelo").focus()

    } else {

        //almacenar información recorriendo las tuplas de la tabla 
        $("#tabla1 tbody>tr").each(function () {

            var clave_catastral = document.getElementById('busqueda').value

            var self_5 = $(this)
            var t_suelo = self_5.find("td:eq(0)").text().trim()
            var valor_has = self_5.find("td:eq(1)").text().trim()
            var has = self_5.find("td:eq(2)").text().trim()
            var a = self_5.find("td:eq(3)").text().trim()
            var c = self_5.find("td:eq(4)").text().trim()


            //condición para los atributos top y vias/c
            if (top.trim() == "" && vias_c.trim() == "") {
                top = "0"
                vias_c = "0"
            } else {
                top = $("#top").val();
                vias_c = $("#vias_c").val();
            }


            var data = { "clave_catatastral_id": clave_catastral, "t_suelo": t_suelo, "valor_has": valor_has, "has": has, "a": a, "c": c, "top": top, "vias_c": vias_c }
            console.log(data)

            $.ajax({
                headers: { 'X-CSRFToken': "{{csrf_token}}" },
                url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosrurales",
                data: data,
                type: "GET",
                success: function (r) {

                    if(response.r==true){
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
        })


        /////////
        if (has_st.trim() == "" && a_st.trim() == "" && c_st.trim() == "") {

            has_st = "0"
            a_st = "0"
            c_st = "0"

        } else {
            has_st = $("#has_st").val();
            a_st = $("#a_st").val();
            c_st = $("#c_st").val();
        }

        var data2 = { "clave_catatastral_id": clave_catastral, "has_st": has_st, "a_st": a_st, "c_st": c_st }

        $.ajax({
            headers: { 'X-CSRFToken': "{{csrf_token}}" },
            url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosrurales_supertotal",
            data: data2,
            type: "GET",
            success: function (r) {

            },
            error: function (jqXHR, textStatus, error) {
                console.log(error)
            },
            complete: function (xhr, status) {
                console.log("finalizado")
            }
        })
    }
}

//Guarda información para terrenos urbanos
function guardar_datosUrbanos () {

    

    //clave catastral Terrenos Urbanos
    var clave_catastral_tu =  document.getElementById('busqueda').value
    var valor2_m2 = $("#valor2_m2").val();
    var area_terreno = $("#area_terreno").val();
    var c_s = $("#c_s").val();
    var valor_m2 = $("#valor_m2").val();
    var frente = $("#frente").val();
    var profundidad = $("#profundidad").val();

    //datos de input de incremento por esquina
    var incremento_A = $("#incremento_A").val();
    var incremento_B = $("#incremento_B").val();
    var incremento_C = $("#incremento_C").val();
    var incremento_D = $("#incremento_D").val();


    //datos de input de demeritos de predios
    var demeritos_interes = $("#demeritos_interes").val();
    var demeritos_excedente = $("#demeritos_excedente").val();
    var demeritos_topografia = $("#demeritos_topografia").val();
    var demeritos_condicion = $("#demeritos_condicion").val();

    //condiciión para el primer apartado de la pantalla
    if (valor2_m2.trim() === "" && area_terreno.trim() === "" && c_s.trim() === "" &&
        valor_m2.trim() === "" && frente.trim() === "" && profundidad.trim() === "") {

        alert("datos vacios")

    } else {
        //recorre las tuplas creadas en la tabla
        $("#tabla tbody>tr").each(function () {
            var self_4 = $(this)
            var c_s = self_4.find("td:eq(0)").text().trim()
            var valor_m2 = self_4.find("td:eq(1)").text().trim()
            var frente = self_4.find("td:eq(2)").text().trim()
            var profundidad = self_4.find("td:eq(3)").text().trim()

            var datos = {
                "clave_catastral_tu": clave_catastral_tu, "valor2_m2": valor2_m2,
                "area_terreno": area_terreno, "c_s": c_s, "valor_m2": valor_m2,
                "frente": frente, "profundidad": profundidad
            }

            //funcion ajax para mandar datos al backend
            $.ajax({
                headers: { 'X-CSRFToken': "{{csrf_token}}" },
                url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosurbanos",
                data: datos,//se envia el arreglo con la información
                type: "GET",
                success: function (r) {

                },
                error: function (jqXHR, textStatus, error) {
                    console.log(error)
                },
                complete: function (xhr, status) {
                    console.log("finalizado")
                }
            })

        })

        //mandar información de tabla incremento por esquina
        $("#t1 tbody>tr").each(function () {
            var self_3 = $(this)
            var tipo_in = self_3.find("td:eq(0)").text().trim()
            var valor_in = self_3.find("td:eq(1)").text().trim()

            console.log(tipo_in + ":" + valor_in)

            var data_increment = { "clave_catastral_tu": clave_catastral_tu, "tipo_in": tipo_in, "valor_in": valor_in }
            $.ajax({
                headers: { 'X-CSRFToken': "{{csrf_token}}" },
                url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosurbanos_incremento",
                data: data_increment,//se envia el arreglo con la información
                type: "GET",
                success: function (r) {

                },
                error: function (jqXHR, textStatus, error) {
                    console.log(error)
                },
                complete: function (xhr, status) {
                    console.log("finalizado")
                }
            })

        })


        //mandar información de tabla demeritos de predios

        $("#t2 tbody>tr").each(function () {
            var self_2 = $(this)
            var descripcion_de = self_2.find("td:eq(0)").text().trim()
            var valor_de = self_2.find("td:eq(1)").text().trim()

            console.log(descripcion_de + ":" + valor_de)

            var data_demerito = { "clave_catastral_tu": clave_catastral_tu, "descripcion_de": descripcion_de, "valor_de": valor_de }
            $.ajax({
                headers: { 'X-CSRFToken': "{{csrf_token}}" },
                url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosurbanos_demeritos",
                data: data_demerito,//se envia el arreglo con la información
                type: "GET",
                success: function (r) {

                },
                error: function (jqXHR, textStatus, error) {
                    console.log(error)
                },
                complete: function (xhr, status) {
                    console.log("finalizado")
                }
            })

        })

    }

}

//Guarda información para datos de construccion
function guardar_datosConstruccion () {

    

    //clave catastral datos de construccion
    var clave_catastral_dc = document.getElementById('busqueda').value

    $("#tabla_construccion tbody>tr").each(function () {
        var self_1 = $(this)
        var etiqueta = self_1.find("td:eq(0)").text().trim()
        var tipo_c = self_1.find("td:eq(1)").text().trim()
        var est = self_1.find("td:eq(2)").text().trim()
        var terreno = self_1.find("td:eq(3)").text().trim()
        var antiguedad = self_1.find("td:eq(4)").text().trim()
        var area_c = self_1.find("td:eq(5)").text().trim()


        var data_construccion = {
            "clave_catastral_dc": clave_catastral_dc, "etiqueta": etiqueta, "tipo_c": tipo_c,
            "est": est, "terreno": terreno, "antiguedad": antiguedad, "area_c": area_c
        }
        $.ajax({
            headers: { 'X-CSRFToken': "{{csrf_token}}" },
            url: "/catastro/catastro/perfil/ficha_catastral/registrar_datosconstruccion",
            data: data_construccion,//se envia el arreglo con la información
            type: "GET",
            success: function (r) {

            },
            error: function (jqXHR, textStatus, error) {
                console.log(error)
            },
            complete: function (xhr, status) {
                console.log("finalizado")
            }
        })

    })
}




