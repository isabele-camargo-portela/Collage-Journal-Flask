from flask import Flask, render_template, request, jsonify

# para criar o hash da senha
from werkzeug.security import generate_password_hash

# importa função de conex]ao
from db import get_connection

# pysql
from pymysql.err import IntegrityError

import re

# para as imagens
import base64

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
def inserir_usuario(nome, email, hash_gerado, imagem_bytes, bio):
    conexao = get_connection()

    try:
        with conexao.cursor() as cursor:             
            cursor.execute(
                "insert into usuario(nome, email, senha, foto, bio) values (%s,%s,%s,%s,%s)",
                (nome, email, hash_gerado, imagem_bytes, bio,)
            )

            conexao.commit()

        return True
    
    except Exception:
        conexao.rollback()
        raise
    
    finally:
        conexao.close()

# insere relato de bug
def inserir_relato(relato):
    conexao = None

    try:
        conexao = get_connection()

        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO relato_bug (relato) VALUES (%s)",
                (relato,)
            )

            conexao.commit()

        return True

    except Exception as erro:
        if conexao:
            conexao.rollback()

        print(f"Erro ao inserir relato: {erro}")

        return False

    finally:
        if conexao:
            conexao.close()

# busca os novos usuarios
def buscar_novos_usuarios():
    conexao = get_connection()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "select nome, foto, bio from usuario order by id_usuario DESC limit 10"
            )

            usuarios = cursor.fetchall()

            for usuario in usuarios:
                if usuario["foto"] == None:
                    usuario["foto"] = "/static/img/avatar-padrao.png"
                else:
                    usuario["foto"] = "data:image/png;base64," + base64.b64encode(
                        usuario["foto"]
                    ).decode("utf-8")

            return usuarios

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

@app.route("/api/novos-usuarios")
def novos_usuarios():
    try:
        usuarios = buscar_novos_usuarios()

        return jsonify({
            "sucesso": True,
            "usuarios": usuarios
        }), 200

    except Exception:
        app.logger.exception("Erro ao buscar novos usuarios.")

        return jsonify({
            "sucesso": False,
            "mensagem": "Não foi possível carregar os usuários."
        }), 500

# forulario de cadastro
@app.route("/api/cadastro", methods=["POST"])
def cadastro_usuario():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha")
    foto = request.files.get("foto")
    bio = request.form.get("bio", "").strip()

    # validação dos campos
    if not nome:
        return jsonify({
            "sucesso": False,
            "campo": "nome",
            "mensagem": "Informe seu nome."
        }), 400

    if len(nome) > 50:
        return jsonify({
            "sucesso": False,
            "campo": "nome",
            "mensagem": "O nome deve ter no máximo 50 caracteres."
        }), 400

    if not email:
        return jsonify({
            "sucesso": False,
            "campo": "email",
            "mensagem": "Informe seu e-mail."
        }), 400

    if len(email) > 100 or not re.match(
        r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email
    ):
        return jsonify({
            "sucesso": False,
            "campo": "email",
            "mensagem": "Informe um e-mail válido."
        }), 400

    if not senha:
        return jsonify({
            "sucesso": False,
            "campo": "senha",
            "mensagem": "Informe sua senha."
        }), 400

    if len(senha) < 8:
        return jsonify({
            "sucesso": False,
            "campo": "senha",
            "mensagem": "A senha deve ter pelo menos 8 caracteres."
        }), 400

    # validação da foto
    imagem_bytes = None

    if foto and foto.filename:

        imagem_bytes = foto.read(5 * 1024 * 1024 + 1)

        if len(imagem_bytes) > 5 * 1024 * 1024:
            return jsonify({
                "sucesso": False,
                "campo": "foto",
                "mensagem": "A imagem deve ter no máximo 5 MB."
            }), 400

        # verifica se é png
        assinatura_png = b"\x89PNG\r\n\x1a\n"

        if not imagem_bytes.startswith(assinatura_png):
            return jsonify({
                "sucesso": False,
                "campo": "foto",
                "mensagem": "Envie uma imagem PNG válida."
            }), 400

    try:

        # Verifica e-mail duplicado
        if email_existe(email):
            return jsonify({
                "sucesso": False,
                "campo": "email",
                "mensagem": "Este e-mail já está cadastrado."
            }), 409

        # Gera o hash da senha
        hash_gerado = senha_hash(senha)

        # envia os dados para a função
        inserir_usuario(nome, email, hash_gerado, imagem_bytes, bio)

        return jsonify({
            "sucesso": True,
            "mensagem": "Cadastro realizado com sucesso!"
        }), 201

    except IntegrityError:

        # Proteção contra duplicidade em requisições simultâneas
        return jsonify({
            "sucesso": False,
            "campo": "email",
            "mensagem": "Este e-mail já está cadastrado."
        }), 409

    except Exception:
        app.logger.exception("Erro ao realizar cadastro.")

        return jsonify({
            "sucesso": False,
            "mensagem": "Não foi possível realizar o cadastro. Tente novamente."
        }), 500
    
# formulario de relato de bugs
@app.route("/api/relato-bug", methods=["POST"])
def receber_relato():

    relato = request.form.get("relato")

    if not relato or not relato.strip():
        return jsonify({
            "sucesso": False,
            "mensagem": "O relato não pode estar vazio."
        }), 400

    resultado = inserir_relato(relato)

    if not resultado:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não foi possível salvar o relato."
        }), 500

    return jsonify({
        "sucesso": True,
        "mensagem": "Relato enviado com sucesso!"
    }), 200

# app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
