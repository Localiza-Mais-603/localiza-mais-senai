
function AlterarTema() {
    document.body.classList.toggle("escuro");
}

const cards = document.querySelectorAll(".card");
const botaoAbrir = document.getElementById("btnAbrir");
const botaoFechar = document.getElementById("btnFechar");
const filtragem = document.getElementById("janelaFiltro");
const modal = document.getElementById("modalCard");

// Abrir janela de filtros
if (botaoAbrir && filtragem) {
    botaoAbrir.addEventListener("click", () => {
        filtragem.classList.add("aberto");
    });
}

// Fechar janela de filtros
if (botaoFechar && filtragem) {
    botaoFechar.addEventListener("click", () => {
        filtragem.classList.remove("aberto");
    });
}

// Filtrar cards por categoria
function Filtrar() {
    const filtros = Array.from(
        document.querySelectorAll(".filtro-categoria:checked")
    ).map(input => input.value);

    cards.forEach(card => {
        const categoria = card.dataset.categoria;

        if (filtros.length === 0 || filtros.includes(categoria)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });

    if (filtragem) {
        filtragem.classList.remove("aberto");
    }
}

// Abrir detalhes do card
function abrirCard(card) {
    document.getElementById("modalTitulo").textContent =
        card.dataset.item || "";

    document.getElementById("modalDescricao").textContent =
        card.dataset.descricao || "";

    document.getElementById("modalLocal").textContent =
        card.dataset.local || "Não informado";

    document.getElementById("modalData").textContent =
        card.dataset.data && card.dataset.data !== "None"
            ? card.dataset.data
            : "Não informada";

    document.getElementById("modalStatus").textContent =
        card.dataset.status || "Não informado";

    // Mostrar foto do item
    const modalFoto = document.getElementById("modalFoto");
    const foto = card.dataset.foto;

    if (foto && foto.trim() !== "" && foto !== "None") {
        modalFoto.onerror = function () {
            modalFoto.style.display = "none";
        };

        modalFoto.onload = function () {
            modalFoto.style.display = "block";
        };

        modalFoto.src = foto;
    } else {
        modalFoto.removeAttribute("src");
        modalFoto.style.display = "none";
    }

    modal.classList.add("aberto");
}

// Fechar detalhes
function fecharCard() {
    modal.classList.remove("aberto");
}

// Fechar ao clicar fora do modal
if (modal) {
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            fecharCard();
        }
    });
}





