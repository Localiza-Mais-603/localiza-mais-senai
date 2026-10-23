function TabButton(type){
    const usuarioBtn = document.querySelector('.tab-buttons button:nth-child(1)');
    const apoioBtn = document.querySelector('.tab-buttons button:nth-child(2)');
    const usuarioForm = document.getElementById('form-usuario');
    const apoioForm = document.getElementById('form-apoio');


    if(type == 'usuario'){
        usuarioBtn.classList.add('active');
        usuarioBtn.classList.remove('active');
        usuarioForm.classList.add('active');
        usuarioForm.classList.remove('active');
    } else if (type == 'apoio'){
        apoioBtn.classList.add('active');
        apoioBtn.classList.remove('active');
        apoioForm.classList.add('active');
        apoioForm.classList.remove('active');

        
    }

}