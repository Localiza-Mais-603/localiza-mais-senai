
  const formsRemover = document.querySelectorAll(".form-remover");
  formsRemover.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const nome = form.dataset.nome || "este coordenador";
      const confirmou = confirm(
        `Tem certeza que deseja remover ${nome}?\nOs itens vinculados a ele permanecerão cadastrados sem coordenador.`
      );

      if (!confirmou) {
        event.preventDefault();
      }
    });
  });


function AlterarTema() {
    document.body.classList.toggle("escuro");

    const modoEscuroAtivo = document.body.classList.contains("escuro");
    localStorage.setItem("tema", modoEscuroAtivo ? "escuro" : "claro");
}

(function carregarTemaSalvo() {
    const temaSalvo = localStorage.getItem("tema");

    if (temaSalvo === "escuro") {
        document.body.classList.add("escuro");
    } else if (temaSalvo === "claro") {
        document.body.classList.remove("escuro");
    }
})();