new Autocomplete('#autocomplete',{
    search : input => {

        //Ruta de la vista donde se consulta la informacion
        const url = `/finanzas/buscar_adeudo/ajax/?search=${input}`

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

        // Ruta asginada para acceder a la vista
        // <a style="text-decoration: none; color: inherit;" href="pago_derechos/${result.clave_catastral}">
        return `
        ${group}
        <a style="text-decoration: none; color: inherit;" href="/finanzas/pago_derechos/${result.clave_catastral}">
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