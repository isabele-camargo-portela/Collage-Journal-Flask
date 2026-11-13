const formularioCadastro = document.getElementById("cadastroForm");

// campos do formulario
const campoNome = document.getElementById("nome");
const campoEmail = document.getElementById("email");
const campoSenha = document.getElementById("senha");
const campoConfirmarSenha = document.getElementById("confirmar_senha");
const campoBio = document.getElementById("bio");

const mensagemStatus = document.getElementById("mensagem-status");

//fução para tratamento de erro
function mostrarMensagem(mensagem, tipo = "erro") {
    mensagemStatus.textContent = mensagem;
    mensagemStatus.style.display = "block";
    mensagemStatus.classList.remove("sucesso", "erro");
    mensagemStatus.classList.add(tipo);
}

function limparErros() {
    document.querySelectorAll(".erro-campo").forEach((elemento) => {
        elemento.textContent = "";
    });

    mensagemStatus.textContent = "";
    mensagemStatus.style.display = "none";
}

function mostrarErroCampo(campo, mensagem) {
    const elemento = document.querySelector(
        `[data-erro-de="${campo}"]`
    );

    if (elemento) {
        elemento.textContent = mensagem;
    }
}

//validação do formulario
formularioCadastro.addEventListener("submit", function(evento) {

    evento.preventDefault();

    limparErros();

    const nome = campoNome.value.trim();
    const email = campoEmail.value.trim();
    const senha = campoSenha.value;
    const confirmar_senha = campoConfirmarSenha.value;
    const bio = campoBio.value;

    let formularioValido = true;

    if(!nome) {
        mostrarErroCampo("nome", "Informe seu nome");
        formularioValido = false;
    }

    if (!email) {
        mostrarErroCampo("email", "Informe seu e-mail.");
        formularioValido = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        mostrarErroCampo("email", "Informe um e-mail válido.");
        formularioValido = false;
    }

    if (!senha) {
        mostrarErroCampo("senha", "Crie uma senha.");
        formularioValido = false;
    }

    else if (senha.length < 8) {
        mostrarErroCampo("senha", "Senha muito curta.");
        formularioValido = false;
    }
        
    if (!confirmar_senha) {
        mostrarErroCampo("confirmar_senha", "Confirme a senha");
        formularioValido = false;
    }

    else if (senha !== confirmar_senha) {
        mostrarErroCampo("confirmar_senha", "As senhas não coincidem.");
        formularioValido = false;
    }

    if (!formularioValido) {
        return;
    }
});