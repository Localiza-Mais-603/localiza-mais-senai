document.addEventListener('submit', function (event) {
    const formulario = event.target;

    // CONFIRMAR ARQUIVAMENTO
    if (formulario.classList.contains('form-arquivar')) {
        event.preventDefault();

        Swal.fire({
            title: 'Arquivar item?',
            text: 'O item será movido para a lista de itens arquivados.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#024873', // Cor adaptada ao seu tema
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sim, arquivar',
            cancelButtonText: 'Cancelar'
        }).then((resultado) => {
            if (resultado.isConfirmed) {
                // Envia os dados silenciosamente via Fetch API
                fetch(formulario.action, {
                    method: formulario.method,
                    body: new FormData(formulario)
                }).then(response => {
                    if (response.ok) {
                        // Mostra o alerta de sucesso e recarrega a página ao fechar
                        Swal.fire({
                            title: 'Arquivado!',
                            text: 'O item foi arquivado com sucesso.',
                            icon: 'success',
                            confirmButtonColor: '#F28705'
                        }).then(() => {
                            window.location.reload(); 
                        });
                    } else {
                        Swal.fire('Erro!', 'Não foi possível arquivar o item.', 'error');
                    }
                }).catch(() => {
                    Swal.fire('Erro!', 'Ocorreu um problema de conexão.', 'error');
                });
            }
        });
    }

    // CONFIRMAR DESARQUIVAMENTO
    if (formulario.classList.contains('form-desarquivar')) {
        event.preventDefault();

        Swal.fire({
            title: 'Desarquivar item?',
            text: 'O item voltará a aparecer na lista principal.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#198754',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sim, desarquivar',
            cancelButtonText: 'Cancelar'
        }).then((resultado) => {
            if (resultado.isConfirmed) {
                fetch(formulario.action, {
                    method: formulario.method,
                    body: new FormData(formulario)
                }).then(response => {
                    if (response.ok) {
                        Swal.fire({
                            title: 'Desarquivado!',
                            text: 'O item foi restaurado com sucesso.',
                            icon: 'success',
                            confirmButtonColor: '#F28705'
                        }).then(() => {
                            window.location.reload();
                        });
                    } else {
                        Swal.fire('Erro!', 'Não foi possível desarquivar o item.', 'error');
                    }
                }).catch(() => {
                    Swal.fire('Erro!', 'Ocorreu um problema de conexão.', 'error');
                });
            }
        });
    }
});