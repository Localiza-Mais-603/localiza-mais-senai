function AlterarTema() {
    const switchDark = document.getElementById("switch-dark-mode");
    const modoEscuroAtivo = switchDark
        ? switchDark.checked
        : !document.body.classList.contains("escuro");

    document.body.classList.toggle("escuro", modoEscuroAtivo);
    localStorage.setItem("tema", modoEscuroAtivo ? "escuro" : "claro");
}

(function carregarTemaSalvo() {
    const temaSalvo = localStorage.getItem("tema");
    const switchDark = document.getElementById("switch-dark-mode");
    const ativarEscuro = temaSalvo === "escuro";

    document.body.classList.toggle("escuro", ativarEscuro);
    if (switchDark) {
        switchDark.checked = ativarEscuro;
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
    const blocoStatus = document.getElementById("blocoStatus");

    const modalTitulo = document.getElementById("modalTitulo");
    const modalData = document.getElementById("modalData");
    const modalDescricao = document.getElementById("modalDescricao");
    const modalLocal = document.getElementById("modalLocal");
    const modalStatus = document.getElementById("modalStatus");
    const modalNome = document.getElementById("modalNome");
    const modalEmail = document.getElementById("modalEmail");

    if (modalTitulo) modalTitulo.textContent = card.dataset.item || "";
    if (modalData) {
        modalData.textContent = card.dataset.data && card.dataset.data !== "None"
            ? card.dataset.data
            : "Não informada";
    }

    // Preenche Relatado por e E-mail (usado na tela de Relatórios)
    if (modalNome) modalNome.textContent = card.dataset.nome || "Desconhecido";
    if (modalEmail) modalEmail.textContent = card.dataset.email || "Não informado";

    if (ehCoordenacao) {
        if (blocoDescricao) blocoDescricao.style.display = "none";
        if (blocoLocal) blocoLocal.style.display = "none";
        if (blocoStatus) blocoStatus.style.display = "none";
    } else {
        if (blocoDescricao) blocoDescricao.style.display = "";
        if (modalDescricao) {
            modalDescricao.textContent = card.dataset.descricao || "Não informada";
        }

        if (blocoLocal) blocoLocal.style.display = "";
        if (modalLocal) {
            modalLocal.textContent = card.dataset.local && card.dataset.local !== "None"
                ? card.dataset.local
                : "Não informado";
        }

        if (blocoStatus) blocoStatus.style.display = "";
        if (modalStatus) {
            modalStatus.textContent = card.dataset.status || "Não informado";
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

    modal.style.display = "";
    modal.classList.add("aberto");
    modal.setAttribute("aria-hidden", "false");
}

function fecharCard() {
    if (!modal) return;
    modal.classList.remove("aberto");
    modal.style.display = "";
    modal.setAttribute("aria-hidden", "true");
}

// Funções do Modal de Edição
function abrirModalEdicao(botao, idItem) {
    const card = botao.closest(".card");

    document.getElementById("editItem").value = card.dataset.item || "";
    document.getElementById("editDescricao").value = card.dataset.descricao || "";
    document.getElementById("editLocal").value = card.dataset.local !== "None" ? card.dataset.local : "";

    let dataValor = card.dataset.data && card.dataset.data !== "None" ? card.dataset.data : "";
    if (dataValor.includes("/")) {
        dataValor = dataValor.split("/").reverse().join("-");
    }
    document.getElementById("editData").value = dataValor;

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
    const inputId = document.getElementById('retirarIdItem');
    const spanNome = document.getElementById('nomeItemRetirada');
    const inputNome = document.getElementById('nomeRetirante');
    const inputEmail = document.getElementById('emailRetirante');

    if (inputId) inputId.value = idItem;
    if (spanNome) spanNome.textContent = nomeItem;
    if (inputNome) inputNome.value = '';
    if (inputEmail) inputEmail.value = '';

    if (modal) {
        modal.classList.add('aberto');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const modalRetirar = document.getElementById('modalRetirarItem');
    const btnFecharRetirar = document.getElementById('btnFecharRetirar');
    const btnCancelarRetirar = document.getElementById('btnCancelarRetirar');
    const formRetirar = document.getElementById('formRetirar');

    // Fechar Modal no X ou Cancelar
    if (btnFecharRetirar && modalRetirar) {
        btnFecharRetirar.addEventListener('click', () => modalRetirar.classList.remove('aberto'));
    }
    if (btnCancelarRetirar && modalRetirar) {
        btnCancelarRetirar.addEventListener('click', () => modalRetirar.classList.remove('aberto'));
    }

    // Fechar ao clicar fora da caixa branca
    if (modalRetirar) {
        modalRetirar.addEventListener('click', function (e) {
            if (e.target === modalRetirar) {
                modalRetirar.classList.remove('aberto');
            }
        });
    }

    // Confirmação SweetAlert antes de enviar
    if (formRetirar) {
        formRetirar.addEventListener('submit', function (e) {
            e.preventDefault();

            const idItem = document.getElementById('retirarIdItem').value;
            if (!idItem) {
                Swal.fire({
                    icon: 'error',
                    title: 'Erro interno',
                    text: 'ID do item não identificado. Feche o modal e tente novamente.',
                    confirmButtonColor: '#F28705'
                });
                return;
            }

            Swal.fire({
                title: 'Finalizar Retirada?',
                text: 'O item será marcado como RETIRADO e movido para a tela de Retirados.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#2B7566',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, registrar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(formRetirar);
                }
            });
        });
    }
});