new Autocomplete('#autocomplete',{
    search : input => {

        const url = `ajax/?search=${input}`

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
        <a style="text-decoration: none; color: inherit;" href="pago_2/${result.clave_catastral}">
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


