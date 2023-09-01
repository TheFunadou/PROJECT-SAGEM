// Después de la inicialización del Autocomplete...
document.getElementById('autocomplete').addEventListener('click', function(event) {
    const target = event.target.closest('a');
    if (target && target.dataset.contribuyente) {
      const contribuyente = JSON.parse(target.dataset.contribuyente);
      // Llenar los campos de texto con la información del contribuyente
      document.getElementById('busqueda').value = contribuyente.clave_catastral;
      document.getElementById('tipopredio').value = contribuyente.tipo_predio;
      document.getElementById('uso').value = contribuyente.uso_predio;

      
      //información del domicilio del predio
      document.getElementById('municipio2').value = contribuyente.municipio;
      document.getElementById('col_fracc').value = contribuyente.col;
      document.getElementById('ciudad2').value = contribuyente.localidad;
      document.getElementById('calle2').value = contribuyente.calle;
      document.getElementById('ne').value = contribuyente.num_ext;
      document.getElementById('ni').value = contribuyente.num_int;



      // Agrega el resto de los campos del contribuyente aquí

      const autocompleteContainer = document.getElementById('resultado');
        while (autocompleteContainer.firstChild) {
            autocompleteContainer.removeChild(autocompleteContainer.firstChild);
        }
    }
  });
  


new Autocomplete('#autocomplete',{
    search : input => {

        const url = `buscar_predio/?search=${input}`

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

                <div> <strong>${result.clave_catastral} / ${result.tipo_predio} ${result.uso_predio} ${result.amaterno}/</strong></div>
                <div><strong>Calle ${result.calle} #${result.num_ext} COL. ${result.col} / ${result.localidad}</strong></div>
            
            </div>     

            
        </li>
        </a>
        `
        

    }

})


