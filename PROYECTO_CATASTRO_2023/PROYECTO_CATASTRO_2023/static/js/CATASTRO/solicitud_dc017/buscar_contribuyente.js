// Después de la inicialización del Autocomplete...
document.getElementById('rfc').addEventListener('click', function(event) {
    const target = event.target.closest('a');
    if (target && target.dataset.contribuyente) {
      const contribuyente = JSON.parse(target.dataset.contribuyente);
      // Llenar los campos de texto con la información del contribuyente
      document.getElementById('busqueda_1').value = contribuyente.rfc;
      document.getElementById('nombre').value = contribuyente.nombre;
      document.getElementById('apellido paterno').value = contribuyente.apaterno;
      document.getElementById('apellido materno').value = contribuyente.amaterno;

      //información del domicilio del contribuyente
      document.getElementById('telefono').value = contribuyente.telefono_movil;
      document.getElementById('calle').value = contribuyente.calle;
      document.getElementById('num_int').value = contribuyente.num_int;
      document.getElementById('num_ext').value = contribuyente.num_ext;
      document.getElementById('codigo_postal').value = contribuyente.cp;
      document.getElementById('colonia_fraccionamiento').value = contribuyente.col;
      document.getElementById('localidad').value = contribuyente.localidad;

 
      // Agrega el resto de los campos del contribuyente aquí

      const autocompleteContainer = document.getElementById('resultado');
        while (autocompleteContainer.firstChild) {
            autocompleteContainer.removeChild(autocompleteContainer.firstChild);
        }
    }
  });
  


new Autocomplete('#rfc',{
    search : input => {

        const url = `buscar_contribuyente/?search=${input}`

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

                <div> <strong>${result.rfc} / ${result.nombre} ${result.apaterno} ${result.amaterno}/</strong></div>
    
            
            </div>     

            
        </li>
        </a>
        `
        

    }

})