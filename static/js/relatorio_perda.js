function abrirCard(elemento) {
    document.getElementById('modalTitulo').innerText = elemento.getAttribute('data-item') || 'Item';
    document.getElementById('modalDescricao').innerText = elemento.getAttribute('data-descricao') || 'Sem descrição.';
    document.getElementById('modalLocal').innerText = elemento.getAttribute('data-local') || 'Não informado';
    document.getElementById('modalData').innerText = elemento.getAttribute('data-data') || 'Não informada';
    document.getElementById('modalStatus').innerText = elemento.getAttribute('data-status') || '';

    document.getElementById('modalEmail').innerText = elemento.getAttribute('data-email') || 'Não informado';
    document.getElementById('modalNome').innerText = elemento.getAttribute('data-nome') || 'Desconhecido';

    const foto = elemento.getAttribute('data-foto');
    const imgElement = document.getElementById('modalFoto');
    if (foto && foto !== "None" && foto !== "") {
        imgElement.src = foto;
        imgElement.style.display = 'block';
    } else {
        imgElement.style.display = 'none';
        imgElement.src = '';
    }

    const modal = document.getElementById('modalCard');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

function fecharCard() {
    const modal = document.getElementById('modalCard');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        fecharCard();
    }
});