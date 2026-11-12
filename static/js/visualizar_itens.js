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

    const ehCoordenacao = card.dataset.coordenacao === "true";
    const blocoDescricao = document.getElementById("blocoDescricao");
    const blocoLocal = document.getElementById("blocoLocal");
    const blocoStatus = document.getElementById("blocoStatus"); // <-- 1. ADICIONADO

    document.getElementById("modalTitulo").textContent = card.dataset.item || "";
    document.getElementById("modalData").textContent = card.dataset.data && card.dataset.data !== "None" ? card.dataset.data : "Não informada";
    // <-- 2. REMOVIDA A LINHA DO modalStatus QUE FICAVA AQUI

    if (ehCoordenacao) {
        if (blocoDescricao) blocoDescricao.style.display = "none";
        if (blocoLocal) blocoLocal.style.display = "none";
        if (blocoStatus) blocoStatus.style.display = "none"; // <-- 3. ADICIONADO (esconde na coordenação)
    } else {
        if (blocoDescricao) {
            blocoDescricao.style.display = "";
            document.getElementById("modalDescricao").textContent = card.dataset.descricao || "Não informada";
        }
        if (blocoLocal) {
            blocoLocal.style.display = "";
            document.getElementById("modalLocal").textContent = card.dataset.local && card.dataset.local !== "None" ? card.dataset.local : "Não informado";
        }
        if (blocoStatus) { // <-- 3. ADICIONADO (mostra nos itens dos alunos)
            blocoStatus.style.display = "";
            document.getElementById("modalStatus").textContent = card.dataset.status || "Não informado";
        }
    }

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

document.addEventListener('DOMContentLoaded', function () {
    const btnFechar = document.getElementById('btnFecharFiltro');
    const janelaFiltro = document.getElementById('janelaFiltro');
    const btnAbrir = document.getElementById('btnAbrir');

    // Função para abrir o filtro
    if (btnAbrir && janelaFiltro) {
        btnAbrir.addEventListener('click', function () {
            janelaFiltro.classList.add('aberto');
            janelaFiltro.style.display = ''; // Limpa qualquer inline style anterior
        });
    }

    // Função para fechar o filtro
    if (btnFechar && janelaFiltro) {
        btnFechar.addEventListener('click', function () {
            janelaFiltro.classList.remove('aberto');
            janelaFiltro.style.display = ''; // Limpa o estilo inline para não bloquear reaberturas
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const modalCadastrar = document.getElementById('modalCadastrarItem');
    const btnAbrirCadastrar = document.getElementById('btnAbrirCadastrar');
    const btnFecharCadastrar = document.getElementById('btnFecharCadastrar');
    const btnCancelarCadastrar = document.getElementById('btnCancelarCadastrar');
    const btnAddCatModal = document.getElementById('btn-abrir-modal');
    const formCadastrar = document.getElementById('formCadastrarItem');

    // 1. Abrir Modal e preencher data de hoje automaticamente
    if (btnAbrirCadastrar && modalCadastrar) {
        btnAbrirCadastrar.addEventListener('click', function () {
            if (formCadastrar) formCadastrar.reset();

            const campoData = document.getElementById('cadData');
            if (campoData) {
                const hoje = new Date();
                hoje.setMinutes(hoje.getMinutes() - hoje.getTimezoneOffset());
                campoData.value = hoje.toISOString().slice(0, 10);
            }

            modalCadastrar.classList.add('aberto');
        });
    }

    // 2. Fechar no botão X ou Cancelar
    if (btnFecharCadastrar && modalCadastrar) {
        btnFecharCadastrar.addEventListener('click', () => modalCadastrar.classList.remove('aberto'));
    }
    if (btnCancelarCadastrar && modalCadastrar) {
        btnCancelarCadastrar.addEventListener('click', () => modalCadastrar.classList.remove('aberto'));
    }

    // 3. Fechar ao clicar fora da caixa branca
    if (modalCadastrar) {
        modalCadastrar.addEventListener('click', function (e) {
            if (e.target === modalCadastrar) {
                modalCadastrar.classList.remove('aberto');
            }
        });
    }

    // 5. Validação da foto e Confirmação com SweetAlert antes de salvar
    if (formCadastrar) {
        formCadastrar.addEventListener('submit', function (e) {
            e.preventDefault();

            // Validação de extensão da foto
            const campoFoto = document.getElementById('cadFoto');
            const extensoesPermitidas = ['png', 'jpg', 'jpeg', 'gif', 'webp'];

            if (campoFoto && campoFoto.files.length > 0) {
                const extensao = campoFoto.files[0].name.split('.').pop().toLowerCase();
                if (!extensoesPermitidas.includes(extensao)) {
                    campoFoto.value = '';
                    Swal.fire({
                        icon: 'error',
                        title: 'Arquivo inválido!',
                        text: 'Selecione somente imagens PNG, JPG, JPEG, GIF ou WEBP.',
                        confirmButtonColor: '#F28705',
                        target: modalCadastrar
                    });
                    return;
                }
            }

            Swal.fire({
                title: 'Confirmar Cadastro?',
                text: 'Tem certeza de que deseja salvar este item no sistema?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#024873',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, cadastrar',
                cancelButtonText: 'Cancelar',
                target: modalCadastrar
            }).then((result) => {
                if (result.isConfirmed) {
                    formCadastrar.submit();
                }
            });
        });
    }
});
// ABRIR MODAL DE RETIRADA
function abrirModalRetirar(idItem, nomeItem) {
    const modal = document.getElementById('modalRetirarItem');
    document.getElementById('retirarIdItem').value = idItem;
    document.getElementById('nomeItemRetirada').textContent = nomeItem;
    document.getElementById('nomeRetirante').value = '';
    document.getElementById('emailRetirante').value = '';
    
    if (modal) {
        modal.classList.add('aberto');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const modalRetirar = document.getElementById('modalRetirarItem');
    const btnFecharRetirar = document.getElementById('btnFecharRetirar');
    const btnCancelarRetirar = document.getElementById('btnCancelarRetirar');
    const formRetirar = document.getElementById('formRetirar');

    // Fechar Modal
    if (btnFecharRetirar && modalRetirar) {
        btnFecharRetirar.addEventListener('click', () => modalRetirar.classList.remove('aberto'));
    }
    if (btnCancelarRetirar && modalRetirar) {
        btnCancelarRetirar.addEventListener('click', () => modalRetirar.classList.remove('aberto'));
    }

    // Confirmação SweetAlert antes de enviar
    if (formRetirar) {
        formRetirar.addEventListener('submit', function (e) {
            e.preventDefault();

            Swal.fire({
                title: 'Finalizar Retirada?',
                text: 'O item será marcado como RETIRADO e movido para a tela de Retirados.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#2B7566',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, registrar',
                cancelButtonText: 'Cancelar',
                target: document.getElementById('modalRetirarItem')
            }).then((result) => {
                if (result.isConfirmed) {
                    formRetirar.submit();
                }
            });
        });
    }
});