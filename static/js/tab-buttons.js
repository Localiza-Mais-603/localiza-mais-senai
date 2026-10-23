
function ButtonsTap(tipo){
    const formUsuario = document.getElementById('form-usuario')
    const formApoio = document.getElementById('form-apoio')

    const botoes = document.querySelectorAll('.tab-buttons')


    botoes.forEach(botao => botao.classList.remove('active'));
    if(formApoio) formApoio.classList.remove('active');
    if (formUsuario) formUsuario.classList.remove('active')


    if(tipo == 'usuario'){
        if(formUsuario) formUsuario.classList.add('active');
        

        botoes[0].classList.add('active')
    } else if(tipo == 'apoio'){
        if(formApoio)formApoio.classList.add('active')

        botoes[1].classList.add('active')
    }
}