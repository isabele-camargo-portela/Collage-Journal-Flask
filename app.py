from flask import Flask, render_template, request, jsonify

# para criar o hash da senha
from werkzeug.security import generate_password_hash

# importa função de conex]ao
from db import get_connection

app = Flask(__name__)


# rotas de teste
@app.route("/api/teste-conexao")
def teste_conexao():
    conexao = None

    try:
        conexao = get_connection()

        return jsonify({
            "mensagem": "Conexão com o banco estabelecida!"
        }), 200

    except Exception as erro:
        return jsonify({
            "mensagem": "Erro ao conectar com o banco.",
            "erro": str(erro)
        }), 500

    finally:
        if conexao:
            conexao.close()

@app.route("/api/teste-email")
def teste_email():
    resultado = email_existe("teste@email.com")

    return jsonify({
        "email_existe": resultado
    })

@app.route("/api/teste-senha")
def teste_senha():
    resultado = senha_hash("minha_senha_teste")

    return jsonify({
        "senha": resultado
    })

@app.route("/api/teste-cadastro")
def teste_cadastro():
    nome = "Usuário Teste"
    email = "teste@email.com"
    hash_gerado = senha_hash("12345678")
    foto = None
    bio = "Teste de cadastro"

    resultado = inserir_usuario(nome, email, hash_gerado, foto, bio)

    return jsonify({
        "cadastro": resultado
    })

# serviços

# verifica email dublicado
def email_existe(email):
    conexao = get_connection()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "select id_usuario from usuario where email = %s",
                (email,)
            )

            resultado = cursor.fetchone()

            return resultado is not None

    finally:
        conexao.close()

# cria o hash da senha
def senha_hash(senha):

    hash_gerado = generate_password_hash(senha)

    return hash_gerado

# função cadastro
def inserir_usuario(nome, email, hash_gerado, foto, bio):
    conexao = get_connection()

    try:
        with conexao.cursor() as cursor:
            if foto:
                imagem_bytes = foto.read()
            else:
                imagem_bytes = None
                
            cursor.execute(
                "insert into usuario(nome, email, senha, foto, bio) values (%s,%s,%s,%s,%s)",
                (nome, email, hash_gerado, imagem_bytes, bio,)
            )

            conexao.commit()

        return True
    
    finally:
        conexao.close()



# rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/make")
def make():
    return render_template("make.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/api/cadastro", methods=["POST"])
def cadastro_usuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    foto = request.files.get("foto")
    bio = request.form.get("bio")

    resultado = email_existe(email)

    if resultado:
        return jsonify({
            "sucesso": False,
            "campo": "email",
            "mensagem": "Este e-mail já está cadastrado."
        }), 409
    else:
        hash_gerado = senha_hash(senha)
        inserir_usuario(nome, email, hash_gerado, foto, bio)

        return jsonify({
            "sucesso": True,
            "mensagem": "Veja seu perfil na área de novos usuários."
        }), 200
    
# app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)