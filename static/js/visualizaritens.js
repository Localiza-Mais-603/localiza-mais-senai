
function AlterarTema(){
    document.body.classList.toggle("escuro")
}

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



