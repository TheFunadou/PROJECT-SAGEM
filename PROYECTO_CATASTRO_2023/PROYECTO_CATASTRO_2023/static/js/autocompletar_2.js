// Después de la inicialización del Autocomplete...
document.getElementById('autocomplete').addEventListener('click', function(event) {
    const target = event.target.closest('a');
    if (target && target.dataset.contribuyente) {
      const contribuyente = JSON.parse(target.dataset.contribuyente);
      // Llenar los campos de texto con la información del contribuyente
      document.getElementById('busqueda').value = contribuyente.clave_catastral;
      document.getElementById('fnombre').value = contribuyente.nombre;
      document.getElementById('fa_paterno').value = contribuyente.apaterno;
      document.getElementById('fa_materno').value = contribuyente.amaterno;
      document.getElementById('fcurp').value = contribuyente.rfc;

      //información del domicilio del contribuyente
      document.getElementById('f_calle_notifica').value = contribuyente.calle_con;
      document.getElementById('f_int_notifica').value = contribuyente.int_con;
      document.getElementById('f_ext_notifica').value = contribuyente.ext_con;
      document.getElementById('f_cp_notifica').value = contribuyente.codigo_postal;
      document.getElementById('f_colonia_fracc_notifica').value = contribuyente.colonia_fraccionamiento_con;
      document.getElementById('f_ciudad_notifica').value = contribuyente.localidad_con;

      //información del domicilio del predio
      document.getElementById('f_calle').value = contribuyente.calle;
      document.getElementById('f_col_fracc').value = contribuyente.colonia;
      document.getElementById('f_ext').value = contribuyente.num_ext;
      document.getElementById('f_int').value = contribuyente.num_int;

      

      // Agrega el resto de los campos del contribuyente aquí

      const autocompleteContainer = document.getElementById('resultado');
        while (autocompleteContainer.firstChild) {
            autocompleteContainer.removeChild(autocompleteContainer.firstChild);
        }
    }
  });
  


new Autocomplete('#autocomplete',{
    search : input => {

        const url = `ajax_ficha/?search=${input}`

        return new Promise(resolve => {
            fetch(url)
            .then(response=>response.json())
            .then(data=>{
                resolve(data.payload)
            })
        })
    },
    renderResult : (result, props) =>{


        let group =''
        if(result.index %3 ==0){
            group = '<li class="group">Group</li>'
        }

        return `
        ${group}
        <a  style="text-decoration: none; color: inherit;" href="javascript:void(0);" data-contribuyente='${JSON.stringify(result)}'">
        <li >
           
 
            <div id="busqueda" class= "miElemento card" style= "font-size:14px;" >

                <div> <strong>${result.clave_catastral} / ${result.nombre} ${result.apaterno} ${result.amaterno}/</strong></div>
                <div><strong>Calle ${result.calle} #${result.num_ext} COL. ${result.colonia} / ${result.localidad}</strong></div>
            
            </div>     

            
        </li>
        </a>
        `
        

    }

})


