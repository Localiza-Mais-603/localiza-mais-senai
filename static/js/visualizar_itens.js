function AlterarTema() {
    document.body.classList.toggle("escuro");

    const modoEscuroAtivo = document.body.classList.contains("escuro");
    localStorage.setItem("tema", modoEscuroAtivo ? "escuro" : "claro");
}

(function carregarTemaSalvo() {
    const temaSalvo = localStorage.getItem("tema");

    if (temaSalvo === "escuro") {
        document.body.classList.add("escuro");
    } else if (temaSalvo === "claro") {
        document.body.classList.remove("escuro");
    }
})();

const modalEdicao = document.getElementById("modalEdicao");
const modal = document.getElementById("modalCard");

document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");
    const botaoAbrir = document.getElementById("btnAbrir");
    const botaoFechar = document.getElementById("btnFechar");
    const filtragem = document.getElementById("janelaFiltro");

    if (botaoAbrir && filtragem) {
        botaoAbrir.addEventListener("click", () => {
            filtragem.classList.add("aberto");
        });
    }

    if (botaoFechar && filtragem) {
        botaoFechar.addEventListener("click", () => {
            filtragem.classList.remove("aberto");
        });
    }

    // Validação de campos obrigatórios no modal de edição
    const formEdicao = document.getElementById("formEdicao");
    if (formEdicao) {
        formEdicao.addEventListener("submit", function (event) {
            const nomeItem = document.getElementById("editItem").value.trim();
            const descricaoItem = document.getElementById("editDescricao").value.trim();

            if (!nomeItem || !descricaoItem) {
                event.preventDefault();
                
                Swal.fire({
                    title: 'Atenção!',
                    text: 'Por favor, preencha os campos obrigatórios: Nome do Item e Descrição.',
                    icon: 'warning',
                    confirmButtonColor: '#F28705'
                });
            }
        });
    }
});

function Filtrar() {
    const cards = document.querySelectorAll(".card");
    const filtragem = document.getElementById("janelaFiltro");

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

function abrirCard(card) {
    if (!modal) return;

    document.getElementById("modalTitulo").textContent = card.dataset.item || "";
    document.getElementById("modalDescricao").textContent = card.dataset.descricao || "";
    document.getElementById("modalLocal").textContent = card.dataset.local || "Não informado";
    document.getElementById("modalData").textContent = card.dataset.data && card.dataset.data !== "None" ? card.dataset.data : "Não informada";
    document.getElementById("modalStatus").textContent = card.dataset.status || "Não informado";

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

function fecharCard() {
    if (modal) modal.classList.remove("aberto");
}

// Funções do Modal de Edição
function abrirModalEdicao(botao, idItem) {
    const card = botao.closest(".card");

    document.getElementById("editItem").value = card.dataset.item || "";
    document.getElementById("editDescricao").value = card.dataset.descricao || "";
    document.getElementById("editLocal").value = card.dataset.local !== "None" ? card.dataset.local : "";
    document.getElementById("editData").value = card.dataset.data !== "None" ? card.dataset.data : "";

    document.getElementById("formEdicao").action = `/atualizar-item/${idItem}`;

    if (modalEdicao) modalEdicao.classList.add("aberto");
}

function fecharModalEdicao() {
    if (modalEdicao) modalEdicao.classList.remove("aberto");
}