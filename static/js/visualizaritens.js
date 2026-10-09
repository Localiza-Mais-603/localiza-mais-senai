
function AlterarTema(){
    document.body.classList.toggle("escuro")

    // verifica se ficou escuro e salva no navegador 

    const isEscuro = document.body.classList.contains("escuro")
    localStorage.setItem("tema", isEscuro ? "escuro" : "claro" )
}


document.addEventListener("DOMContentLoaded", ()=>{
    const temaSalvo = localStorage.getItem("tema")
    if(temaSalvo == "escuro"){
        document.body.classList.add("escuro")
    }

})

const botaoAbrir = document.getElementById('btnAbrir')
const botaoFechar = document.getElementById('btnFechar')
const filtragem = document.getElementById('janelaFiltro')


botaoAbrir.addEventListener('click', () =>{
    filtragem.classList.add('aberto')
}
)


botaoFechar.addEventListener('click', () =>{
    filtragem.classList.remove('aberto')
})



