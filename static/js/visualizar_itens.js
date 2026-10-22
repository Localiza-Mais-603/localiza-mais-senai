
function AlterarTema(){
    document.body.classList.toggle("escuro")
}

const cards = document.querySelectorAll(".card")
const botaoAbrir = document.getElementById('btnAbrir')
const botaoFechar = document.getElementById('btnFechar')
const filtragem = document.getElementById('janelaFiltro')

// Ele irá percorrer cada um dos cards encontrados, e impede o comportamento dessa tag

cards.forEach(card => {
    card.addEventListener('click', (event) =>{
        event.preventDefault()
    })
})


botaoAbrir.addEventListener('click', () =>{
    filtragem.classList.add('aberto')
}
)


botaoFechar.addEventListener('click', () =>{
    filtragem.classList.remove('aberto')
})





function Filtrar(){
    // Ele irá buscar apenas os filtros que estão com as caixas marcadas, e tambem ele irá apenas extrair o texto do value de cada caixa selecionada
    const filtros = Array.from(document.querySelectorAll('.grupo-conteudo input:checked')).map(i => i.value)

    cards.forEach(card =>{
        const categoria = card.getAttribute('data-categoria')

        const data = card.getAttribute('data-data')
        

        if(filtros.length === 0 || filtros.includes(categoria)){
            card.style.display = 'block'
        } else {
            card.style.display = 'none'
        }
    })

    if(filtragem){
        filtragem.classList.remove('aberto');
    }
    


}


