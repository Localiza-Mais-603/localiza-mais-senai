
document.addEventListener("DOMContentLoaded", function () {
    const elementoMensagens = document.getElementById("flash-messages");

    if (!elementoMensagens) {
        return;
    }

    const mensagens = JSON.parse(elementoMensagens.textContent);

    mensagens.forEach(function ([categoria, mensagem]) {
        Swal.fire({
            title: categoria === "success" ? "Sucesso!" : "Erro!",
            text: mensagem,
            icon: categoria === "success" ? "success" : "error",
            confirmButtonText: "OK",
            confirmButtonColor: "#C20000"
        });
    });
});

