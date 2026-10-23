document.addEventListener('DOMContentLoaded', () => {
    configurarModalCategoria();
});

function configurarModalCategoria() {
    // Seleciona os elementos
    const modal = document.getElementById('modal-categoria');
    const btnAbrir = document.getElementById('btn-abrir-modal');
    const btnFechar = document.getElementById('btn-fechar-modal');
    const btnCancelar = document.getElementById('btn-cancelar-modal');
    const formModal = document.getElementById('form-cadastrar-categoria');
    const inputNome = document.getElementById('nova-categoria-nome');
    const selectCategoria = document.getElementById('categoria');

    //  Abrir e fechar a janela
    const abrirModal = () => {
        modal.style.display = 'flex';
        inputNome.value = ''; 
        inputNome.focus();
    };

    const fecharModal = () => {
        modal.style.display = 'none';
        inputNome.value = '';
    };

    if (btnAbrir) btnAbrir.addEventListener('click', abrirModal);
    if (btnFechar) btnFechar.addEventListener('click', fecharModal);
    if (btnCancelar) btnCancelar.addEventListener('click', fecharModal);

    // Fechar o model se o usuário apertar na parte externa
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            fecharModal();
        }
    });

    // Enviar a nova categoria para o back-end
    if (formModal) {
        formModal.addEventListener('submit', async (e) => {
            e.preventDefault(); // Impede a página de recarregar

            const nomeCategoria = inputNome.value.trim();

            if (!nomeCategoria) return;

            try {
                const resposta = await fetch('/api/categorias', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome: nomeCategoria })
                });

                const resultado = await resposta.json();

                if (resultado.sucesso) {
                    // Cria uma nova categoria
                    const novaOpcao = document.createElement('option');
                    novaOpcao.value = resultado.id_categoria;
                    novaOpcao.textContent = resultado.nome;
                    novaOpcao.selected = true; // Seleciona automaticamente a categoria criada

                    // Adiciona a categoria
                    selectCategoria.appendChild(novaOpcao);
                    fecharModal();
                } else {
                    alert('Erro ao cadastrar categoria: ' + (resultado.mensagem || 'Tente novamente.'));
                }
            } catch (erro) {
                console.error('Erro na requisição:', erro);
                alert('Falha ao ligar ao servidor.');
            }
        });
    }
}