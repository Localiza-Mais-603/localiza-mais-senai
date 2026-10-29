

document.addEventListener('DOMContentLoaded', () => {
    // Captura do botão e do campo select do teu HTML
    const btnAbrir = document.getElementById('btn-abrir-modal');
    const selectCategoria = document.getElementById('categoria');

    if (btnAbrir) {
        btnAbrir.addEventListener('click', () => {
            // Dispara o modal do SweetAlert2
            Swal.fire({
                title: 'Cadastrar Nova Categoria',
                input: 'text',
                inputLabel: 'Nome da Categoria',
                inputPlaceholder: 'Ex: Eletrónicos, Documentos...',
                showCancelButton: true,
                confirmButtonText: 'Salvar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#ff3b3b', // Cor vermelha compatível com o teu tema
                cancelButtonColor: '#296fad',
                
                // Validação: Impede enviar o campo em branco
                inputValidator: (valor) => {
                    if (!valor || !valor.trim()) {
                        return 'Por favor, digite o nome da categoria!';
                    }
                },
                
                // Processamento assíncrono antes de fechar o modal
                showLoaderOnConfirm: true,
                preConfirm: async (nomeCategoria) => {
                    try {
                        const resposta = await fetch('/api/categorias', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ nome: nomeCategoria.trim() })
                        });

                        const resultado = await resposta.json();

                        if (!resposta.ok || !resultado.sucesso) {
                            throw new Error(resultado.mensagem || 'Erro ao cadastrar categoria.');
                        }

                        return resultado; // Retorna os dados (id_categoria e nome)
                    } catch (erro) {
                        Swal.showValidationMessage(`Falha: ${erro.message}`);
                    }
                },
                allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                // Se o utilizador clicou em "Salvar" e a API respondeu com sucesso
                if (result.isConfirmed && result.value) {
                    const dados = result.value;

                    // Criar e selecionar a nova opção no <select> do formulário
                    const novaOpcao = document.createElement('option');
                    novaOpcao.value = dados.id_categoria;
                    novaOpcao.textContent = dados.nome;
                    novaOpcao.selected = true; // Seleciona automaticamente a categoria criada

                    selectCategoria.appendChild(novaOpcao);

                    // Alerta rápido de confirmação
                    Swal.fire({
                        icon: 'success',
                        title: 'Sucesso!',
                        text: 'Categoria adicionada com sucesso.',
                        timer: 1500,
                        showConfirmButton: false
                    });
                }
            });
        });
    }
});