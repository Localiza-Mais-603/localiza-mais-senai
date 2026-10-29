document.addEventListener('DOMContentLoaded', function () {

    const formularios = document.querySelectorAll('.form-excluir');

    formularios.forEach(function (form) {

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            event.stopPropagation();

            Swal.fire({
                title: 'Tem certeza?',
                text: 'Deseja excluir este item permanentemente?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, excluir!',
                cancelButtonText: 'Cancelar',
                reverseButtons: true
            }).then(function (resultado) {

                if (resultado.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(form);
                }

            });
        });

    });

});