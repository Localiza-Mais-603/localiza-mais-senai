document.addEventListener("DOMContentLoaded", () => {
  
  // 1. BOTÃO EXCLUIR (Tabela de Analistas)
  const formsRemover = document.querySelectorAll(".form-remover");
  formsRemover.forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const nome = form.dataset.nome || "este analista";

      Swal.fire({
        title: `Excluir ${nome}?`,
        text: "Os itens vinculados a ele permanecerão cadastrados sem analista.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#e03c3e",
        cancelButtonColor: "#64748b",
        confirmButtonText: "Sim, excluir",
        cancelButtonText: "Cancelar",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          form.submit();
        }
      });
    });
  });

  // 2. BOTÃO SALVAR / CADASTRAR (Modal Novo Analista)
  const formCadastrar = document.getElementById("formCadastrarCoor");
  if (formCadastrar) {
    formCadastrar.addEventListener("submit", (event) => {
      event.preventDefault();

      Swal.fire({
        title: "Confirmar cadastro?",
        text: "Deseja cadastrar este novo analista no sistema?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#0b4a7d",
        cancelButtonColor: "#64748b",
        confirmButtonText: "Sim, cadastrar",
        cancelButtonText: "Revisar",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          formCadastrar.submit();
        }
      });
    });
  }

  // 3. BOTÃO SALVAR ALTERAÇÕES (Modal Editar)
  const formEditar = document.getElementById("formEditarCoor");
  if (formEditar) {
    formEditar.addEventListener("submit", (event) => {
      event.preventDefault();

      Swal.fire({
        title: "Salvar alterações?",
        text: "As informações deste perfil serão atualizadas.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#0b4a7d",
        cancelButtonColor: "#64748b",
        confirmButtonText: "Sim, salvar",
        cancelButtonText: "Continuar editando",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          formEditar.submit();
        }
      });
    });
  }

  // 4. BOTÕES CANCELAR (Dentro dos Modais)
  const botoesCancelar = document.querySelectorAll(".modal .btn-cancelar");
  botoesCancelar.forEach((btn) => {
    // Garante que o Bootstrap não feche o modal antes do alerta
    btn.removeAttribute("data-bs-dismiss");

    btn.addEventListener("click", () => {
      const modalEl = btn.closest(".modal");
      const modalInstance = bootstrap.Modal.getInstance(modalEl);

      Swal.fire({
        title: "Descartar alterações?",
        text: "Os dados preenchidos serão perdidos.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#e03c3e",
        cancelButtonColor: "#64748b",
        confirmButtonText: "Sim, descartar",
        cancelButtonText: "Voltar",
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed && modalInstance) {
          modalInstance.hide();
          const form = modalEl.querySelector("form");
          if (form) form.reset();
        }
      });
    });
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