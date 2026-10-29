document.querySelectorAll('.form-excluir').forEach(form => {

    form.addEventListener('submit', function (event) {

        event.preventDefault();
        event.stopPropagation();

        Swal.fire({
            title: 'Tem certeza?',
            text: 'Essa ação excluirá o item permanentemente!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sim, excluir!',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then((resultado) => {

            if (resultado.isConfirmed) {
                form.submit();
            }

        });

    });

});