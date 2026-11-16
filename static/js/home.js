const cards = document.getElementById("perfis");
const left = document.getElementById("left");
const right = document.getElementById("right");

async function carregarUsuarios() {

    try {
        const resposta = await fetch("/api/novos-usuarios");
        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.mensagem);
        }

        cards.innerHTML = "";

        if (resultado.usuarios.length === 0) {
            cards.textContent = "Ainda não temos usuários cadastrados.";
            return;
        }

        resultado.usuarios.forEach(function(usuario) {

            const card = document.createElement("article");
            card.classList.add("card-perfil");

            if (usuario.foto) {
                const foto = document.createElement("img");
                foto.src = usuario.foto;
                foto.alt = "Foto de perfil de " + usuario.nome;
                foto.classList.add("foto-perfil");

                card.appendChild(foto);

            } else {
                const semFoto = document.createElement("div");
                semFoto.classList.add("sem-foto");
                semFoto.textContent = usuario.nome.charAt(0).toUpperCase();

                card.appendChild(semFoto);
            }

            const nome = document.createElement("h6");
            nome.textContent = usuario.nome;

            const bio = document.createElement("p");
            bio.textContent = usuario.bio || "Este usuário ainda não adicionou uma bio.";

            card.appendChild(nome);
            card.appendChild(bio);

            cards.appendChild(card);

        });

    }
    catch (erro) {
        console.error("Erro ao carregar usuários:", erro);
        cards.textContent = "Não foi possível carregar os usuários.";
    }
}

right.addEventListener("click", function() {
    cards.scrollBy({
        left: 300,
        behavior: "smooth"
    });
});

left.addEventListener("click", function() {
    cards.scrollBy({
        left: -300,
        behavior: "smooth"
    });
});

carregarUsuarios();