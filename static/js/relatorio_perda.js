function abrirCardRelatorio(elemento) {
    const modal = document.getElementById('modalCard');
    if (!modal) return;

    const setTexto = (id, valor) => {
        const el = document.getElementById(id);
        if (el) el.textContent = valor;
    };

    setTexto('modalTitulo', elemento.dataset.item || 'Item');
    setTexto('modalNome', elemento.dataset.nome || 'Desconhecido');
    setTexto('modalEmail', elemento.dataset.email || 'Não informado');
    setTexto('modalDescricao', elemento.dataset.descricao || 'Sem descrição.');
    setTexto('modalLocal', elemento.dataset.local || 'Não informado');
    setTexto('modalData', elemento.dataset.data || 'Não informada');
    setTexto('modalStatus', elemento.dataset.status || 'Perdido');

    const foto = elemento.dataset.foto;
    const imgElement = document.getElementById('modalFoto');
    if (imgElement) {
        if (foto && foto !== 'None' && foto.trim() !== '') {
            imgElement.src = foto;
            imgElement.style.display = 'block';
        } else {
            imgElement.removeAttribute('src');
            imgElement.style.display = 'none';
        }
    }

    modal.classList.add('aberto');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

function fecharCardRelatorio() {
    const modal = document.getElementById('modalCard');
    if (!modal) return;

    modal.classList.remove('aberto');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        fecharCardRelatorio();
    }
});