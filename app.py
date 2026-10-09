from flask import Flask, render_template, request, redirect, url_for, session
from model.cadastro import cadastrar_usuario, cadastrar_coor
from model.cadastrar_itens import cadastrar_item
from model.login import verificar_login_coor, verificar_login_usuario


app = Flask(__name__)

app.secret_key = "chciclete"

@app.route("/")
def index():
    return render_template("index.html")

# login usuario
@app.route("/login/usuario", methods=["GET", "POST"])
def pag_login_aluno():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = verificar_login_usuario(email, senha)

        if usuario:
          
            session["usuario"] = usuario 
            
            return redirect(url_for("pag_inicial_usuario"))
        else:
            erro = "E-mail ou senha incorretos!"

    return render_template("login-usuario.html", erro=erro)



@app.route("/tela-corporativa")
def pag_tela_corporativa():
    return render_template("tela-inicial-corporativo.html") 
    
@app.route("/login/setor/de/apoio", methods=["GET", "POST"])
def pag_login_coordenacao():
    erro = None
    
    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]

       
        coordenador = verificar_login_coor(cpf, senha)

        if coordenador:
           
            return redirect(url_for("pag_tela_corporativa"))
        else:
         
            erro = "CPF ou senha incorretos!"

  
    return render_template("login-coor.html", erro=erro)


# Selecionar perfil
@app.route("/selecionar/perfil")
def pag_selecionar_perfil():
    return redirect('selecionar-perfil.html')


#CADASTRO USUARIO
@app.route("/cadastro/usuario") 
def pag_cadastro(): 
    return render_template("cadastrar_usuario.html") 

@app.route("/cadastro", methods=["POST"]) 
def cadastro(): 
    cpf = request.form["CPF"] 
    nome = request.form["nome_completo"] 
    curso = request.form["curso"] 
    email = request.form["email"] 
    senha = request.form["senha"] 
    cadastrar_usuario(cpf, nome, curso, email, senha) 
    return redirect("/cadastro/usuario")

@app.route('/cadastro-coor', methods=['GET', 'POST'])
def cadastro_coor():
    if request.method == 'POST':
        nome = request.form['nome_completo']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']

        cadastrar_coor(nome, cpf, email, senha)

        return redirect('/login/setor/de/apoio')

    return render_template('cadastro_coordenacao.html')

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

@app.route("/tela/inicial/corporativo")
def tela_inicial_corporativo():
    return render_template("tela-inicial-corporativo.html")
    
@app.route("/tela/inicial/usuario")
def pag_inicial_usuario():
    return render_template("tela_inicial_usuario.html")


@app.route("/visualizar-perfil")
def visualizar_perfil():
    return render_template("visualizar_perfil.html")

@app.route("/editar/perfil")
def editar_perfil():
    return render_template("editar-perfil.html")


@app.route("/visualizar-itens")
def visualizar_itens():
    return render_template("visualizar_itens.html")


if __name__ == "__main__":
    app.run(debug=True)