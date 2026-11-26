(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        const form = document.getElementById('pesqForm');
        const campo = document.getElementById('pesqCampo');
        const limpar = document.getElementById('pesqLimpar');
        const contador = document.getElementById('pesqContador');
        const lista = document.querySelector('.itens-card');

        if (!form || !campo || !lista) return;

        const ehCoordenacao = document.body.classList.contains('pagina-coordenacao');

        // Tira acentos e maiúsculas para comparar
        function norm(texto) {
            return (texto || '').toString()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .toLowerCase();
        }

        // Evita que o texto digitado vire HTML
        function esc(texto) {
            return String(texto).replace(/[&<>"']/g, function (c) {
                return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
            });
        }

        // Nome de cada categoria, lido da janela de filtros
        const nomesCategoria = {};

        document.querySelectorAll('#janelaFiltro input[name="categoria"]').forEach(function (input) {
            const rotulo = input.closest('label');
            nomesCategoria[input.value] = rotulo ? rotulo.textContent.trim() : '';
        });

        // Texto pesquisável de cada item da lista
        const itens = Array.from(lista.querySelectorAll(':scope > li')).map(function (li) {
            const card = li.querySelector('.card');
            const d = card ? card.dataset : {};

            return {
                li: li,
                texto: norm([
                    d.item, d.descricao, d.local, d.publicado,
                    d.destino, d.status, nomesCategoria[d.categoria]
                ].join(' '))
            };
        });

        // Área do aviso "item não cadastrado"
        const vazio = document.createElement('div');
        vazio.className = 'pesq-vazio';
        vazio.hidden = true;
        lista.insertAdjacentElement('afterend', vazio);

        // Itens realmente visíveis (considera também o filtro de data)
        function contarVisiveis() {
            return itens.filter(function (i) { return i.li.offsetParent !== null; }).length;
        }

        function avisoNaoCadastrado(termo) {

            const acaoPrincipal = ehCoordenacao
                ? '<button type="button" class="pesq-btn pesq-btn-main" data-acao="cadastrar">Cadastrar este item</button>'
                : '<button type="button" class="pesq-btn pesq-btn-main" data-acao="perdi">Relatar que perdi isso</button>';

            const dica = ehCoordenacao
                ? ''
                : '<p class="pesq-vazio-sub">Perdeu algo assim? Relate a perda e a coordenação procura para você.</p>';

            return '<div class="pesq-vazio-icone"><i class="fa-solid fa-box-open" aria-hidden="true"></i></div>' +
                '<h3 class="pesq-vazio-titulo">“' + esc(termo) + '” ainda não foi cadastrado</h3>' +
                '<p class="pesq-vazio-sub">Ninguém registrou esse item nos achados e perdidos até agora.</p>' +
                dica +
                '<div class="pesq-vazio-acoes">' + acaoPrincipal +
                '<button type="button" class="pesq-btn" data-acao="limpar">Limpar pesquisa</button></div>';
        }

        function avisoForaDoFiltro(termo) {
            return '<div class="pesq-vazio-icone"><i class="fa-solid fa-filter" aria-hidden="true"></i></div>' +
                '<h3 class="pesq-vazio-titulo">Há itens com “' + esc(termo) + '”, mas fora do filtro atual</h3>' +
                '<p class="pesq-vazio-sub">Ajuste a data ou os filtros para vê-los.</p>' +
                '<div class="pesq-vazio-acoes">' +
                '<button type="button" class="pesq-btn" data-acao="limpar">Limpar pesquisa</button></div>';
        }

        function atualizar() {

            const termo = campo.value.trim();
            const buscando = termo !== '';
            const n = contarVisiveis();

            // Itens que combinam com a pesquisa, mesmo os escondidos por outros filtros
            const combinam = itens.filter(function (i) {
                return !i.li.classList.contains('pesq-oculto');
            }).length;

            if (buscando) {
                contador.textContent = n + (n === 1 ? ' item encontrado' : ' itens encontrados');
            } else {
                contador.textContent = n + (n === 1 ? ' item disponível' : ' itens disponíveis');
            }

            if (n > 0) {
                vazio.hidden = true;
                return;
            }

            if (n > 0 || !buscando) {
                vazio.hidden = true;
                return;
            }

            if (combinam === 0) {
                vazio.innerHTML = avisoNaoCadastrado(termo);
            } else {
                vazio.innerHTML = avisoForaDoFiltro(termo);
            }

            vazio.hidden = false;
        }

        function filtrar() {

            const termos = norm(campo.value).split(/\s+/).filter(Boolean);

            limpar.hidden = !campo.value;

            itens.forEach(function (item) {
                const combina = termos.every(function (t) { return item.texto.includes(t); });
                item.li.classList.toggle('pesq-oculto', !combina);
            });

            atualizar();
        }

        /* ---------- Botões do aviso ---------- */
        function abrirPerdi(termo) {

            const modal = document.getElementById('modalPerdi');

            if (!modal || !window.bootstrap) return;

            // Preenche depois de abrir, porque o formulário é limpo ao abrir
            modal.addEventListener('shown.bs.modal', function () {
                const campoNome = document.getElementById('perdItem');

                if (campoNome) {
                    campoNome.value = termo.slice(0, 50);
                    campoNome.focus();
                }
            }, { once: true });

            bootstrap.Modal.getOrCreateInstance(modal).show();
        }

        function abrirCadastrar(termo) {

            const botao = document.getElementById('btnAbrirCadastrar');

            if (!botao) return;

            botao.click();

            setTimeout(function () {
                const campoNome = document.getElementById('cadItem');

                if (campoNome) {
                    campoNome.value = termo.slice(0, 50);
                    campoNome.focus();
                }
            }, 150);
        }

        vazio.addEventListener('click', function (e) {

            const botao = e.target.closest('[data-acao]');

            if (!botao) return;

            const termo = campo.value.trim();

            if (botao.dataset.acao === 'limpar') {
                campo.value = '';
                filtrar();
                campo.focus();
            } else if (botao.dataset.acao === 'perdi') {
                abrirPerdi(termo);
            } else if (botao.dataset.acao === 'cadastrar') {
                abrirCadastrar(termo);
            }
        });

        /* ---------- Campo de pesquisa ---------- */
        campo.addEventListener('input', filtrar);

        limpar.addEventListener('click', function () {
            campo.value = '';
            filtrar();
            campo.focus();
        });

        campo.addEventListener('keydown', function (e) {
            if (e.key !== 'Escape') return;

            if (campo.value) {
                campo.value = '';
                filtrar();
            } else {
                campo.blur();
            }
        });

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            campo.blur();
        });

        // Tecla "/" leva o cursor para a pesquisa
        document.addEventListener('keydown', function (e) {

            if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;

            const alvo = e.target;

            if (alvo.matches && alvo.matches('input, textarea, select, [contenteditable]')) return;

            e.preventDefault();
            campo.focus();
        });

        // Se o filtro de data mudar, recalcula
        const data = document.getElementById('data');

        if (data) {
            ['change', 'input'].forEach(function (evento) {
                data.addEventListener(evento, function () { setTimeout(atualizar, 80); });
            });
        }

        // Aceita link com ?q=texto (ex.: vindo de outra página)
        const q = new URLSearchParams(window.location.search).get('q');

        if (q) {
            campo.value = q;
            filtrar();
        } else {
            atualizar();
        }
    });
})();