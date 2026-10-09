
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



