from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
def cadastrar_usuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    bio = request.form.get("bio")

    foto = request.files.get("foto")

    return jsonify({
        "mensagem": "Dados recebidos com sucesso!"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)