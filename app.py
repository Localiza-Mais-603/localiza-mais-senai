from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# login usuario
@app.route("/login/usuario")
def pag_login_aluno():
    return render_template("login-usuario.html")

# login coordenacao
@app.route("/login/setor/de/apoio")
def pag_login_coordenacao():
    return render_template("login-coor.html")

# CADASTRO USUARIO
@app.route("/cadastro/usuario")
def pag_cadastro():
    return render_template("cadastro_usuario.html")

# editar itens cadastrado
@app.route("/editar-itens-cadastrado")
def pag_editar_item_cadastrado():
    return render_template("editar-item-cadastrado.html")
















if __name__ == "__main__":
    app.run(debug=True)