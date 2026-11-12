document.addEventListener('DOMContentLoaded', function () {
    // 1. Extensão da função abrirCard para preencher dados da retirada
    const originalAbrirCard = window.abrirCard;

    window.abrirCard = function (el) {
        if (typeof originalAbrirCard === 'function') {
            originalAbrirCard(el);
        } else {
            document.getElementById('modalTitulo').textContent = el.dataset.item || '';
            const foto = document.getElementById('modalFoto');
            if (el.dataset.foto) {
                foto.src = el.dataset.foto;
                foto.style.display = 'block';
            } else {
                foto.style.display = 'none';
            }
            document.getElementById('modalCard').classList.add('aberto');
        }

        // Oculta campos vazios (ex: itens cadastrados pela coordenação)
        const desc = el.dataset.descricao;
        document.getElementById('blocoDescricao').style.display = desc ? '' : 'none';
        document.getElementById('modalDescricao').textContent = desc;

        const local = el.dataset.local;
        document.getElementById('blocoLocal').style.display = local ? '' : 'none';
        document.getElementById('modalLocal').textContent = local;

        const dataEnc = el.dataset.data;
        document.getElementById('blocoData').style.display = dataEnc ? '' : 'none';
        document.getElementById('modalData').textContent = dataEnc;

        const publicador = el.dataset.publicado;
        const blocoPub = document.getElementById('blocoPublicador');
        if (publicador) {
            document.getElementById('modalPublicador').textContent = publicador;
            blocoPub.style.display = '';
        } else {
            blocoPub.style.display = 'none';
        }

        // Preenche Status e Dados da Retirada
        document.getElementById('modalStatus').textContent = el.dataset.status || 'RETIRADO';
        document.getElementById('modalRetiradoPor').textContent = el.dataset.retirante || 'Não informado';
        document.getElementById('modalEmailRetirante').textContent = el.dataset.emailRetirante || 'Não informado';
        document.getElementById('modalDataRetirada').textContent = el.dataset.dataRetirada || 'Não informada';
    };

    // 2. Exibição das mensagens flash do Flask via SweetAlert2
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer && flashContainer.dataset.messages) {
        try {
            const messages = JSON.parse(flashContainer.dataset.messages);
            messages.forEach(([category, message]) => {
                if (category === 'success') {
                    Swal.fire({
                        title: 'Sucesso!',
                        text: message,
                        icon: 'success',
                        confirmButtonColor: '#F28705'
                    });
                } else if (category === 'error') {
                    Swal.fire({
                        title: 'Erro!',
                        text: message,
                        icon: 'error',
                        confirmButtonColor: '#dc3545'
                    });
                }
            });
        } catch (e) {
            console.error('Erro ao processar mensagens flash:', e);
        }
    }
});