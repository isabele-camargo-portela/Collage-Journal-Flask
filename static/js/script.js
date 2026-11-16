const formularioBug = document.getElementById("bugForm");

const campoRelato = document.getElementById("bugDescription");

const feedbackBug = document.getElementById("bugFeedback");

const modalBug = document.getElementById("bugModal");


if (formularioBug) {

    formularioBug.addEventListener("submit", async function(evento) {

        evento.preventDefault();

        const relato = campoRelato.value.trim();

        if (!relato) {
            return;
        }

        const dadosBug = new FormData();

        dadosBug.append("relato", relato);

        try {

            const resposta = await fetch("/api/relato-bug", {
                method: "POST",
                body: dadosBug
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                feedbackBug.textContent = resultado.mensagem;
                feedbackBug.classList.remove("d-none");
                return;
            }

            feedbackBug.textContent = resultado.mensagem;
            feedbackBug.classList.remove("d-none");

            formularioBug.reset();

        } catch (erro) {

            console.error("Erro ao enviar relato:", erro);

            feedbackBug.textContent = "Não foi possível enviar o relato.";
            feedbackBug.classList.remove("d-none");
        }

    });

}


if (modalBug) {

    modalBug.addEventListener("hidden.bs.modal", () => {

        feedbackBug.classList.add("d-none");

        formularioBug.reset();

    });

}
