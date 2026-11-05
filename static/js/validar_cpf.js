function aplicarMascaraCPF(input) {
    let valor = input.value.replace(/\D/g, "");
    
    if (valor.length > 11) {
        valor = valor.substring(0, 11);
    }

    if (valor.length > 9) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*$/, "$1.$2.$3-$4");
    } else if (valor.length > 6) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{3}).*$/, "$1.$2.$3");
    } else if (valor.length > 3) {
        valor = valor.replace(/^(\d{3})(\d{3})/, "$1.$2");
    }
    
    input.value = valor;
}
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
    
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
    }
    
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
    }
    
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}
document.addEventListener("DOMContentLoaded", function() {
    const formCadastro = document.querySelector("form");
    const inputCpf = document.querySelector("input[name='CPF']") || document.querySelector("input[name='cpf']");

    if (inputCpf) {
        inputCpf.addEventListener("input", function() {
            aplicarMascaraCPF(this);
        });
    }

    if (formCadastro && inputCpf) {
        formCadastro.addEventListener("submit", function(event) {
            let cpfLimpo = inputCpf.value;
            
            if (!validarCPF(cpfLimpo)) {
                event.preventDefault();
                
                Swal.fire({
                    icon: 'error',
                    title: 'CPF Inválido',
                    text: 'Por favor, insira um CPF real e válido para continuar.',
                    confirmButtonColor: '#3085d6'
                });
            }
        });
    }
});