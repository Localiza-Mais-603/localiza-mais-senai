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
            confirmButtonColor: '#024873',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sim, arquivar',
            cancelButtonText: 'Cancelar'
        }).then((resultado) => {
            if (resultado.isConfirmed) {
                fetch(formulario.action, {
                    method: formulario.method,
                    body: new FormData(formulario)
                }).then(response => {
                    if (response.ok) {
                        Swal.fire({
                            title: 'Arquivado!',
                            text: 'O item foi arquivado com sucesso.',
                            icon: 'success',
                            showConfirmButton: false,
                            timer: 1500,
                            timerProgressBar: true
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
                            showConfirmButton: false,
                            timer: 1500,
                            timerProgressBar: true
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

function confirmarExclusao(event, form) {
    event.preventDefault();

    Swal.fire({
        title: 'Tem certeza?',
        text: 'Você não poderá reverter a exclusão deste relato!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit();
        }
    });
}

function mostrarAlertaFlash(categoria, mensagem) {
    Swal.fire({
        icon: categoria === 'success' ? 'success' : 'error',
        title: mensagem,
        timer: 2500,
        showConfirmButton: false
    });
}