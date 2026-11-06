function ButtonsTap(tipo){
    const formUsuario = document.getElementById('form-usuario');
    const formApoio = document.getElementById('form-apoio');
    const botoes = document.querySelectorAll('.tab-buttons');

    botoes.forEach(botao => botao.classList.remove('active'));
    if(formApoio) formApoio.classList.remove('active');
    if (formUsuario) formUsuario.classList.remove('active');

    if(tipo === 'usuario'){
        if(formUsuario) formUsuario.classList.add('active');
        if(botoes[0]) botoes[0].classList.add('active');
    } else if(tipo === 'apoio'){
        if(formApoio) formApoio.classList.add('active');
        if(botoes[1]) botoes[1].classList.add('active');
    }
}

// Ativa a aba correta automaticamente com base no parâmetro URL ou rota atual
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const perfilParam = urlParams.get('perfil');
    const path = window.location.pathname;

    if (perfilParam === 'apoio' || path.includes('/setor/de/apoio')) {
        ButtonsTap('apoio');
    } else if (perfilParam === 'usuario' || path.includes('/usuario')) {
        ButtonsTap('usuario');
    }
});