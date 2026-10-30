document.addEventListener("DOMContentLoaded", () => {
    const btnAbrirModal = document.getElementById("btn-abrir-modal");

    if (btnAbrirModal) {
        btnAbrirModal.addEventListener("click", async () => {
            const { value: nomeCategoria } = await Swal.fire({
                title: 'Cadastrar Nova Categoria',
                input: 'text',
                inputLabel: 'Nome da Categoria:',
                inputPlaceholder: 'Ex: Eletrônicos, Roupas, Documentos...',
                showCancelButton: true,
                confirmButtonText: 'Salvar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#0b3c5d',
                inputValidator: (value) => {
                    if (!value || !value.trim()) {
                        return 'Você precisa digitar o nome da categoria!';
                    }
                }
            });

            if (nomeCategoria) {
                try {
                    const response = await fetch('/api/categorias', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nome: nomeCategoria.trim() })
                    });

                    const result = await response.json();

                    if (response.ok && result.sucesso) {
                        // Tenta encontrar pelo ID "categoria" ou pelo ID "id_categoria"
                        const selectCategoria = document.getElementById("categoria") || document.getElementById("id_categoria");
                        
                        if (selectCategoria) {
                            const novaOpcao = document.createElement("option");
                            novaOpcao.value = result.id_categoria;
                            novaOpcao.textContent = result.nome;
                            novaOpcao.selected = true;

                            selectCategoria.appendChild(novaOpcao);
                        }

                        Swal.fire({
                            icon: 'success',
                            title: 'Sucesso!',
                            text: 'Categoria adicionada com sucesso!',
                            timer: 1800,
                            showConfirmButton: false
                        });
                    } else {
                        Swal.fire('Erro!', result.mensagem || 'Não foi possível salvar a categoria.', 'error');
                    }
                } catch (error) {
                    console.error("Erro no fetch:", error);
                    Swal.fire('Erro!', 'Ocorreu uma falha ao se comunicar com o servidor.', 'error');
                }
            }
        });
    }
});