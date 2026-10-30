/* ==========================================================
   GERENCIAMENTO DE TEMA (MODO ESCURO / CLARO)
   ========================================================== */

function AlterarTema() {
    document.body.classList.toggle("escuro");

    const modoEscuroAtivo = document.body.classList.contains("escuro");
    localStorage.setItem("tema", modoEscuroAtivo ? "escuro" : "claro");
}

// Executa imediatamente ao carregar o script para aplicar o tema salvo
(function carregarTemaSalvo() {
    const temaSalvo = localStorage.getItem("tema");

    if (temaSalvo === "escuro") {
        document.body.classList.add("escuro");
    } else if (temaSalvo === "claro") {
        document.body.classList.remove("escuro");
    }
})();

/* ==========================================================
   MANIPULAÇÃO DA INTERFACE E MODAIS
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
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

    // Fechar janela de filtros (se o botão existir)
    if (botaoFechar && filtragem) {
        botaoFechar.addEventListener("click", () => {
            filtragem.classList.remove("aberto");
        });
    }

    // Fechar modal ao clicar na área escura de fora
    if (modal) {
        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                fecharCard();
            }
        });
    }
});

/* ==========================================================
   FUNÇÕES GLOBAIS (FILTROS E MODAL)
   ========================================================== */

// Filtrar cards por categoria
function Filtrar() {
    const cards = document.querySelectorAll(".card");
    const filtragem = document.getElementById("janelaFiltro");

    // Busca checkboxes marcados na janela de filtros
    const filtros = Array.from(
        document.querySelectorAll(".grupo-conteudo input:checked")
    ).map(input => input.value);

    cards.forEach(card => {
        const categoria = card.getAttribute("data-categoria") || card.dataset.categoria;

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

// Abrir detalhes do card no Modal
function abrirCard(card) {
    const modal = document.getElementById("modalCard");
    if (!modal) return;

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

    // Exibição da foto do item
    const modalFoto = document.getElementById("modalFoto");
    const foto = card.dataset.foto;

    if (modalFoto) {
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
    }

    modal.classList.add("aberto");
}

// Fechar Modal
function fecharCard() {
    const modal = document.getElementById("modalCard");
    if (modal) {
        modal.classList.remove("aberto");
    }
}