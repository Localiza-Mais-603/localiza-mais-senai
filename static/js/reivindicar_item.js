document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.form-reivindicar').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var nomeItem = form.querySelector('input[name="nome_item"]').value;

            Swal.fire({
                title: 'Esse item é seu?',
                html: 'Vamos avisar a coordenação que você solicitou o item <strong></strong>.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#024873',
                confirmButtonText: 'Sim, é meu',
                cancelButtonText: 'Cancelar',
                didOpen: function (popup) {
                    // textContent evita problema com caracteres especiais no nome do item
                    popup.querySelector('strong').textContent = nomeItem;
                }
            }).then(function (result) {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
});