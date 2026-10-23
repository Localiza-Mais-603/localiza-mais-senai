from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from model.cadastro import cadastrar_usuario, cadastrar_coor

from model.login import verificar_login_coor, verificar_login_usuario, salvar_token_recuperacao, verificar_token_valido, atualizar_senha_por_token
from dotenv import load_dotenv
from model.login import verificar_login_coor, verificar_login_usuario
from model.cadastrar_itens import cadastrar_item, registrar_item_perdido
from model.listar_itens import listar_todos
from model.visualizar_perfil import buscar_usuario_por_email
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)

app.secret_key = "chciclete"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


app.config['MAIL_USERNAME'] = 'localizamaisararaquara@gmail.com'  
app.config['MAIL_PASSWORD'] = 'rffwsrozekhyezce'  
app.config['MAIL_DEFAULT_SENDER'] = ('Localiza+', 'localizamaisararaquara@gmail.com')


mail = Mail(app)
gerador_de_token = URLSafeTimedSerializer(app.secret_key)






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

    return render_template("login-usuario.html", erro=erro, tipo='usuario')



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

  
    return render_template("login-coor.html", erro=erro, tipo='apoio')


# Selecionar perfil
@app.route("/selecionar/perfil")
def pag_selecionar_perfil():
    return redirect('selecionar-perfil.html')

# CADASTRO USUARIO
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
    return redirect("/login/usuario")

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

# tela seleção de perfil
@app.route("/selecionar-perfil")
def selecionar_perfil():
    return render_template("selecionar-perfil.html")

@app.route("/cadastrar/item")
def pag_cadastrar_item():
    return render_template("registrar_item_perdido.html")

@app.route("/tela/inicial/corporativo")
def tela_inicial_corporativo():
    return render_template("tela-inicial-corporativo.html")
    
@app.route("/tela/inicial/usuario")
def pag_inicial_usuario():
    return render_template("tela_inicial_usuario.html")

@app.route("/visualizar-perfil")
def visualizar_perfil():
    usuario_sessao = session.get("usuario")
    
    if not usuario_sessao:
        return redirect(url_for("pag_login_aluno"))
    email = usuario_sessao.get("email") if isinstance(usuario_sessao, dict) else usuario_sessao[0]
    
    usuario_atualizado = buscar_usuario_por_email(email)
    
    return render_template("visualizar_perfil.html", usuario=usuario_atualizado)


@app.route("/editar/perfil")
def editar_perfil():
    return render_template("editar-perfil.html")



@app.route("/visualizar-itens")
def visualizar_itens():
    itens = listar_todos()
    return render_template("visualizar_itens.html",
                           itens = itens)


@app.route("/cadastrar/item/salvar", methods=["POST"])
def salvar_item():
    produto = request.form["produto"]
    local = request.form["local"]
    data = request.form.get("data")
    descricao = request.form["descricao"]
    cadastrar_item(produto, descricao, local, data)

    return redirect("/cadastrar/item")



@app.route("/registro/itens", methods=["GET", "POST"])
def registrar_itens():
    if request.method == "POST":
        item = request.form.get("item")
        local = request.form.get("local")
        data_encontrado = request.form.get("data")  
        if data_encontrado == "":
            data_encontrado = None
        descricao = request.form.get("descricao")
        email = session["usuario"].get("email")
        nome_foto = None
        foto = request.files.get("foto")

       

        if foto and foto.filename != "":
            nome_foto = secure_filename(foto.filename)
            
            pasta_destino = os.path.join("static", "img_upload")
            os.makedirs(pasta_destino, exist_ok=True)
       
            caminho_completo = os.path.join(pasta_destino, nome_foto)
            foto.save(caminho_completo)

        registrar_item_perdido(
            item=item,
            descricao=descricao,
            data_encontrado=data_encontrado,
            status="Perdido",
            id_categoria=1,
            local=local,
            foto=nome_foto,
            email=email,
            cpf_coordenador=None
        )


        return redirect(url_for("registrar_itens"))

    return render_template("registrar_item_perdido.html")




@app.route("/recuperar-senha", methods=["GET", "POST"])
def pag_recuperar_senha():
    erro = None
    sucesso = None
    
    if request.method == "POST":
        email = request.form.get("email")
        token_gerado = gerador_de_token.dumps(email, salt='recuperar-senha-salt')
        
        try:
            salvar_token_recuperacao(email, token_gerado)
            link_recuperacao = url_for('pag_nova_senha', token=token_gerado, _external=True)
            msg = Message(
                subject="Localiza+ - Recuperação de Senha",
                recipients=[email]
            )
            msg.body = f"Olá!\n\nPara redefinir sua senha no Localiza+, clique no link abaixo:\n\n{link_recuperacao}\n\nSe você não solicitou essa alteração, ignore este e-mail."
            mail.send(msg)
            
            sucesso = "O link de recuperação foi enviado para o seu e-mail!"
        except Exception as e:
            print("\n ERRO DETALHADO NO ENVIO:", e, "\n")
            erro = "Ocorreu um erro ao processar a recuperação de senha."


    return render_template('recuperar-senha.html', erro=erro, sucesso=sucesso)


@app.route("/nova-senha/<token>", methods=["GET", "POST"])
def pag_nova_senha(token):
    erro = None
    usuario_valido = verificar_token_valido(token)
    
    if not usuario_valido:
        return "<h3>Link inválido ou expirado!</h3>", 400
    
    if request.method == "POST":
        nova_senha = request.form.get("nova_senha")
        confirmar_senha = request.form.get("confirmar_senha")
        if nova_senha != confirmar_senha:
            erro = "As senhas não coincidem! Tente novamente."
            return render_template('nova-senha.html', erro=erro, token=token)
            
        atualizar_senha_por_token(token, nova_senha)
        return redirect(url_for('pag_login_aluno'))

    return render_template('nova-senha.html', erro=erro, token=token)





if __name__ == "__main__":
    app.run(debug=True)