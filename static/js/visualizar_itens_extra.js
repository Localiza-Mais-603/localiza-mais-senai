document.addEventListener('DOMContentLoaded', function () {

        // 1. PÍLULA DE PRAZO (SWEETALERT EXPLICATIVO)
    const btnPrazo = document.getElementById('btnPrazoRetirada');
    if (btnPrazo) {
        btnPrazo.addEventListener('click', function () {
            const PRAZO_DIAS = Number(btnPrazo.dataset.prazoDias) || 180;
            const PRAZO_MESES = Number(btnPrazo.dataset.prazoMeses) || 6;
            const PRAZO_MARMITA = Number(btnPrazo.dataset.prazoMarmita) || 0;
            const PRAZO_REDUZIDO = Number(btnPrazo.dataset.prazoReduzido) || 0;
            const trechoVerde = Math.max(PRAZO_DIAS - 30, 1);

            // Aviso das exceções (marmitas e falta de espaço)
            let excecoes = '';

            if (PRAZO_MARMITA) {
                excecoes += `
                    <li><strong>Marmitas:</strong> ficam guardadas por apenas
                    <strong>${PRAZO_MARMITA} ${PRAZO_MARMITA === 1 ? 'dia' : 'dias'}</strong>,
                    por serem perecíveis.</li>`;
            }

            if (PRAZO_REDUZIDO) {
                excecoes += `
                    <li><strong>Falta de espaço:</strong> no momento, o prazo foi reduzido para
                    <strong>${PRAZO_REDUZIDO} dias</strong> porque o espaço de armazenamento está cheio.</li>`;
            } else {
                excecoes += `
                    <li><strong>Falta de espaço:</strong> se o espaço de armazenamento ficar cheio,
                    o prazo poderá ser reduzido.</li>`;
            }

            Swal.fire({
                title: 'Prazo de retirada',
                width: 540,
                confirmButtonText: 'Entendi',
                confirmButtonColor: '#F28705',
                html: `
                    <p style="margin: 0 0 14px; color: #555; font-size: 0.95rem;">
                        Os itens ficam disponíveis por <strong>${PRAZO_MESES} meses</strong>,
                        contados a partir do dia em que foram encontrados.
                    </p>

                    <ul style="margin: 0 0 18px; padding-left: 18px; text-align: left; color: #555; font-size: 0.9rem;">
                        ${excecoes}
                    </ul>

                    <div class="barra-prazo">
                        <span style="flex: ${trechoVerde}; background: #2B7566;"></span>
                        <span style="flex: 23; background: #F28705;"></span>
                        <span style="flex: 7; background: #DC3545;"></span>
                    </div>

                    <div class="legenda-prazo">
                        <div>
                            <i style="background: #2B7566;"></i>
                            <b>Tranquilo</b>
                            <small>mais de 30 dias</small>
                        </div>
                        <div>
                            <i style="background: #F28705;"></i>
                            <b>Atenção</b>
                            <small>30 dias ou menos</small>
                        </div>
                        <div>
                            <i style="background: #DC3545;"></i>
                            <b>Última chamada</b>
                            <small>7 dias ou menos</small>
                        </div>
                        <div>
                            <i style="background: #6c757d;"></i>
                            <b>Descartado</b>
                            <small>após o prazo</small>
                        </div>
                    </div>

                    <p style="margin: 0; color: #555; font-size: 0.9rem;">
                        Reconheceu o seu? Procure a coordenação para retirá-lo.
                    </p>
                `
            });
        });
    }
    // 2. EXTENSÃO DO MODAL DE DETALHES (PUBLICADO POR + DESTINO + PRAZO)
    const originalAbrirCard = window.abrirCard;
    if (typeof originalAbrirCard === 'function') {
        window.abrirCard = function (el) {
            originalAbrirCard(el);

            const nome = el.dataset.publicado;
            const blocoPub = document.getElementById('blocoPublicador');
            if (blocoPub) {
                if (nome) {
                    document.getElementById('modalPublicador').textContent = nome;
                    blocoPub.style.display = '';
                } else {
                    blocoPub.style.display = 'none';
                }
            }

            const destino = el.dataset.destino;
            const blocoDest = document.getElementById('blocoDestino');
            if (blocoDest) {
                if (destino) {
                    document.getElementById('modalDestino').textContent = destino;
                    blocoDest.style.display = '';
                } else {
                    blocoDest.style.display = 'none';
                }
            }

            const prazo = el.dataset.prazo;
            const blocoPrazo = document.getElementById('blocoPrazo');
            if (blocoPrazo) {
                if (prazo) {
                    document.getElementById('modalPrazo').textContent = prazo;
                    blocoPrazo.style.display = '';
                } else {
                    blocoPrazo.style.display = 'none';
                }
            }
        };
    }

    // 3. ADICIONAR CATEGORIA (BOTÕES INLINE NOS MODAIS)
    document.querySelectorAll('.btn-add-cat-inline').forEach(btn => {
        btn.addEventListener('click', async function () {
            const selectId = btn.dataset.selectId;
            const modalId = btn.dataset.modalId;
            const modalTarget = document.getElementById(modalId);

            const resultado = await Swal.fire({
                title: 'Adicionar categoria',
                input: 'text',
                inputLabel: 'Nome da categoria',
                inputAttributes: { maxlength: 50 },
                showCancelButton: true,
                confirmButtonText: 'Adicionar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#F28705',
                target: modalTarget,
                inputValidator: (valor) => {
                    if (!valor || !valor.trim()) {
                        return 'Digite o nome da categoria';
                    }
                }
            });

            if (!resultado.isConfirmed) return;

            try {
                const resp = await fetch('/api/categorias', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome: resultado.value.trim() })
                });

                const dados = await resp.json();

                if (!resp.ok || !dados.sucesso) {
                    throw new Error(dados.mensagem || 'Erro');
                }

                document.querySelectorAll('.select-categoria').forEach(sel => {
                    sel.add(new Option(dados.nome, dados.id_categoria));
                });

                const selectAlvo = document.getElementById(selectId);
                if (selectAlvo) selectAlvo.value = dados.id_categoria;

                Swal.fire({
                    icon: 'success',
                    title: 'Categoria adicionada!',
                    confirmButtonColor: '#F28705',
                    target: modalTarget
                });
            } catch (erro) {
                Swal.fire({
                    icon: 'error',
                    title: 'Erro ao adicionar',
                    text: 'Não foi possível adicionar a categoria. Tente novamente.',
                    confirmButtonColor: '#F28705',
                    target: modalTarget
                });
            }
        });
    });

    // 4. MODAL "PERDI ALGO": RESET E VALIDAÇÃO DE FOTO
    const modalPerdi = document.getElementById('modalPerdi');
    const formPerdi = document.getElementById('formPerdi');
    const campoFoto = document.getElementById('perdFoto');

    if (modalPerdi && formPerdi) {
        modalPerdi.addEventListener('show.bs.modal', () => {
            formPerdi.reset();
            const d = new Date();
            d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
            document.getElementById('perdQuando').value = d.toISOString().slice(0, 10);
        });
    }

    if (formPerdi && campoFoto) {
        const extensoesPermitidas = ['png', 'jpg', 'jpeg', 'gif', 'webp'];

        formPerdi.addEventListener('submit', function (event) {
            if (campoFoto.files.length > 0) {
                const arquivo = campoFoto.files[0];
                const extensao = arquivo.name.split('.').pop().toLowerCase();

                if (!extensoesPermitidas.includes(extensao)) {
                    event.preventDefault();
                    campoFoto.value = '';

                    Swal.fire({
                        icon: 'error',
                        title: 'Arquivo inválido!',
                        text: 'Selecione somente imagens PNG, JPG, JPEG, GIF ou WEBP.',
                        confirmButtonColor: '#F28705',
                        target: modalPerdi
                    });
                }
            }
        });
    }

    // 5. MODAL "ENCONTREI ALGO": RESET E CAMPO "OUTRO"
    const modalEncontrei = document.getElementById('modalEncontrei');
    if (modalEncontrei) {
        const form = modalEncontrei.querySelector('form');
        const outro = document.getElementById('encOutro');

        modalEncontrei.addEventListener('show.bs.modal', () => {
            form.reset();
            outro.classList.add('d-none');
            outro.required = false;

            const d = new Date();
            d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
            document.getElementById('encQuando').value = d.toISOString().slice(0, 10);
        });

        form.querySelectorAll('input[name="destino"]').forEach(r => {
            r.addEventListener('change', () => {
                const selecionado = form.querySelector('input[name="destino"]:checked');
                const isOutro = selecionado && selecionado.value === 'outro';

                outro.classList.toggle('d-none', !isOutro);
                outro.required = isOutro;

                if (isOutro) outro.focus();
            });
        });
    }

    // 6. EXCLUIR CATEGORIA: CONFIRMAÇÃO
    document.querySelectorAll('.form-excluir-categoria').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            Swal.fire({
                title: 'Excluir a categoria "' + form.dataset.nome + '"?',
                text: 'Os itens dessa categoria continuarão cadastrados, mas ficarão sem categoria.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, excluir',
                cancelButtonText: 'Cancelar',
                target: document.getElementById('modalCategorias')
            }).then((resultado) => {
                if (resultado.isConfirmed) form.submit();
            });
        });
    });

    // 7. MENSAGENS FLASH DO FLASK (SWEETALERT2)
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer && flashContainer.dataset.messages) {
        try {
            const messages = JSON.parse(flashContainer.dataset.messages);
            messages.forEach(([category, message]) => {
                if (category === 'success') {
                    Swal.fire({
                        title: 'Sucesso!',
                        text: message,
                        icon: 'success',
                        confirmButtonColor: '#F28705'
                    });
                } else if (category === 'error') {
                    Swal.fire({
                        title: 'Erro!',
                        text: message,
                        icon: 'error',
                        confirmButtonColor: '#dc3545'
                    });
                }
            });
        } catch (e) {
            console.error('Erro ao ler mensagens flash:', e);
        }
    }

    // 8. LOGOUT COM CONFIRMAÇÃO
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) {
        btnLogout.addEventListener('click', function (event) {
            event.preventDefault();

            Swal.fire({
                title: 'Deseja sair da sua conta?',
                text: 'Você precisará fazer login novamente para acessar o sistema.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, sair',
                cancelButtonText: 'Cancelar'
            }).then((resultado) => {
                if (resultado.isConfirmed) {
                    window.location.href = '/logout';
                }
            });
        });
    }

    // 9. FILTRO DE DATA NA TELA
    const inputData = document.getElementById('data');
    const cards = document.querySelectorAll('.itens-card > li');

    if (inputData) {
        function filtrar() {
            const dataFiltro = inputData.value;

            cards.forEach((li) => {
                const card = li.querySelector('.card');
                let dataItem = card ? (card.dataset.data || '') : '';

                if (dataItem.includes('/')) {
                    dataItem = dataItem.split('/').reverse().join('-');
                }

                if (!dataFiltro || dataItem >= dataFiltro) {
                    li.style.display = '';
                } else {
                    li.style.display = 'none';
                }
            });
        }

        inputData.addEventListener('change', filtrar);
        filtrar();
    }
});