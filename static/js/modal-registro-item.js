document.addEventListener("DOMContentLoaded", () => {
    const btnAbrirModal = document.getElementById("btn-abrir-modal");

    if (btnAbrirModal) {
        btnAbrirModal.addEventListener("click", async () => {
            const { value: nomeCategoria } = await Swal.fire({
                title: 'Cadastrar Nova Categoria',
                input: 'text',
                inputLabel: 'Nome da Categoria:',
                inputPlaceholder: 'Ex: Eletrônicos, Roupas, Documentos...',
                showCancelButton: true,
                confirmButtonText: 'Salvar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#0b3c5d',
                inputValidator: (value) => {
                    if (!value || !value.trim()) {
                        return 'Você precisa digitar o nome da categoria!';
                    }
                }
            });

            if (nomeCategoria) {
                try {
                    const response = await fetch('/api/categorias', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nome: nomeCategoria.trim() })
                    });

                    const result = await response.json();

                    if (response.ok && result.sucesso) {
                        // Tenta encontrar pelo ID "categoria" ou pelo ID "id_categoria"
                        const selectCategoria = document.getElementById("categoria") || document.getElementById("id_categoria");
                        
                        if (selectCategoria) {
                            const novaOpcao = document.createElement("option");
                            novaOpcao.value = result.id_categoria;
                            novaOpcao.textContent = result.nome;
                            novaOpcao.selected = true;

                            selectCategoria.appendChild(novaOpcao);
                        }

                        Swal.fire({
                            icon: 'success',
                            title: 'Sucesso!',
                            text: 'Categoria adicionada com sucesso!',
                            timer: 1800,
                            showConfirmButton: false
                        });
                    } else {
                        Swal.fire('Erro!', result.mensagem || 'Não foi possível salvar a categoria.', 'error');
                    }
                } catch (error) {
                    console.error("Erro no fetch:", error);
                    Swal.fire('Erro!', 'Ocorreu uma falha ao se comunicar com o servidor.', 'error');
                }
            }
        });
    }
});

const formulario = document.querySelector(".formulario-perda");

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    Swal.fire({
        title: "Deseja cadastrar este item?",
        text: "Confira se todas as informações estão corretas.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#198754",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim, enviar",
        cancelButtonText: "Cancelar"
    }).then((resultado) => {

        if (resultado.isConfirmed) {
            formulario.submit();
        }

    });

});


// Mensagens enviadas pelo Flask
const mensagens = document.getElementById("flash-messages");

if (mensagens) {

    const flashMessages = JSON.parse(mensagens.textContent);

    flashMessages.forEach(([categoria, mensagem]) => {

        if (categoria === "success") {

            Swal.fire({
                title: "Cadastrado com sucesso!",
                text: mensagem,
                icon: "success",
                confirmButtonColor: "#198754",
                confirmButtonText: "OK"
            });

        } else if (categoria === "error" || categoria === "danger") {

            Swal.fire({
                title: "Erro!",
                text: mensagem,
                icon: "error",
                confirmButtonColor: "#d33",
                confirmButtonText: "OK"
            });

        }

    });

}

const inputFoto = document.getElementById("foto");

if (inputFoto) {
    inputFoto.addEventListener("change", function () {
        const arquivo = inputFoto.files[0];
        if (!arquivo) return;

        const tiposPermitidos = ["image/png", "image/jpeg", "image/gif", "image/webp"];
        const tamanhoMaximo = 5 * 1024 * 1024; // 5 MB

        if (!tiposPermitidos.includes(arquivo.type)) {
            Swal.fire("Formato inválido!", "Envie apenas imagens PNG, JPG, GIF ou WEBP.", "error");
            inputFoto.value = "";   // limpa o campo
            return;
        }

        if (arquivo.size > tamanhoMaximo) {
            Swal.fire("Arquivo muito grande!", "A imagem deve ter no máximo 5 MB.", "error");
            inputFoto.value = "";
        }
    });
}
