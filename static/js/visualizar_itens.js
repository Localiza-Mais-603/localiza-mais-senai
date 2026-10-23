
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

/* =========================
   FILTRO
========================= */

const btnAbrir = document.getElementById("btnAbrir");

const btnFechar = document.getElementById("btnFechar");

const janelaFiltro = document.getElementById("janelaFiltro");


btnAbrir.addEventListener("click", function () {

    janelaFiltro.classList.add("aberto");

});


btnFechar.addEventListener("click", function () {

    janelaFiltro.classList.remove("aberto");

});


/* =========================
   FILTRAR ITENS
========================= */

function Filtrar() {

    const categoriasSelecionadas =
        document.querySelectorAll(".filtro-categoria:checked");


    const categorias = [];


    categoriasSelecionadas.forEach(function (checkbox) {

        categorias.push(checkbox.value);

    });


    const cards =
        document.querySelectorAll(".itens-card .card");


    cards.forEach(function (card) {

        const categoria =
            card.getAttribute("data-categoria");


        if (categorias.length === 0) {

            card.style.display = "flex";

        }

        else if (categorias.includes(categoria)) {

            card.style.display = "flex";

        }

        else {

            card.style.display = "none";

        }

    });


    janelaFiltro.classList.remove("aberto");

}


/* =========================
   ABRIR ITEM
========================= */

function abrirCard(card) {

    document.getElementById("modalTitulo").textContent =
        card.dataset.item;


    document.getElementById("modalDescricao").textContent =
        card.dataset.descricao;


    document.getElementById("modalLocal").textContent =
        card.dataset.local;


    document.getElementById("modalData").textContent =
        card.dataset.data;


    document.getElementById("modalStatus").textContent =
        card.dataset.status;


    document.getElementById("modalCard").classList.add("aberto");

}


/* =========================
   FECHAR ITEM
========================= */

function fecharCard() {

    document.getElementById("modalCard").classList.remove("aberto");

}


/* =========================
   FECHAR CLICANDO NO FUNDO
========================= */

document.getElementById("modalCard").addEventListener("click", function () {

    fecharCard();

});


/* =========================
   MODO ESCURO
========================= */

function AlterarTema() {

    document.body.classList.toggle("escuro");

}

