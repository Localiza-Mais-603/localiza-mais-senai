

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
                confirmButtonColor: '#313b97', 
                cancelButtonColor: '#216097',
                

                inputValidator: (valor) => {
                    if (!valor || !valor.trim()) {
                        return 'Por favor, digite o nome da categoria!';
                    }
                },
                
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

                        return resultado; 
                    } catch (erro) {
                        Swal.showValidationMessage(`Falha: ${erro.message}`);
                    }
                },
                allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                if (result.isConfirmed && result.value) {
                    const dados = result.value;
                    const novaOpcao = document.createElement('option');
                    novaOpcao.value = dados.id_categoria;
                    novaOpcao.textContent = dados.nome;
                    novaOpcao.selected = true; 

                    selectCategoria.appendChild(novaOpcao);

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