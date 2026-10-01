from flask import Flask, render_template, redirect, request
from model import cadastrar_usuario

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


#CADASTRO USUARIO
@app.route("/cadastro/usuario") 
def pag_cadastro(): 
    return render_template("cadastro_usuario.html") 

@app.route("/cadastro", methods=["POST"]) 
def cadastro(): 
    cpf = request.form["CPF"] 
    nome = request.form["nome_completo"] 
    curso = request.form["curso"] 
    email = request.form["email"] 
    senha = request.form["senha"] 
    cadastrar_usuario(cpf, nome, curso, email, senha) 
    return redirect("/cadastro/usuario")

# editar itens cadastrado
@app.route("/editar-item-cadastrado")
def pag_editar_item_cadastrado():
    return render_template("editar-item-cadastrado.html")

#tela seleção de perfil
@app.route("/selecionar-perfil")
def selecionar_perfil():
    return render_template("selecionar-perfil.html")


@app.route("/cadastrar/item")
def pag_cadastrar_item():
    return render_template("cadastrar_itens.html")



@app.route("/cadastrar/item/salvar", methods=["POST"])
def salvar_item():
    produto = request.form["produto"]
    local = request.form["local"]
    data = request.form["data"]
    descricao = request.form["descricao"]

    cadastrar_item(produto, local, data, descricao)

    return redirect("/cadastrar/item")
















if __name__ == "__main__":
    app.run(debug=True)