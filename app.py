from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from model.cadastro import cadastrar_usuario, cadastrar_coor

from model.login import verificar_login_coor, verificar_login_usuario, salvar_token_recuperacao, verificar_token_valido, atualizar_senha_por_token
from model.cadastrar_itens import cadastrar_item, registrar_item_perdido

import os
from werkzeug.utils import secure_filename



app = Flask(__name__)

app.secret_key = "chciclete"

# CONFIGURAÇÃO DE E-MAIL REAL (GMAIL)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Coloque o e-mail da sua equipe ou do projeto Localiza+
app.config['MAIL_USERNAME'] = 'seu_email_do_tcc@gmail.com'  

# ⚠️ NÃO É A SENHA NORMAL DO SEU E-MAIL! 
# É uma "Senha de App" de 16 letras gerada dentro da sua Conta Google
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'  

# Define quem está enviando por padrão
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email_do_tcc@gmail.com'  

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
    return render_template("visualizar_perfil.html")

@app.route("/editar/perfil")
def editar_perfil():
    return render_template("editar-perfil.html")


@app.route("/visualizar-itens")
def visualizar_itens():
    return render_template("visualizar_itens.html")

# ROTA ÚNICA DE SALVAR ITEM
@app.route("/cadastrar/item/salvar", methods=["POST"])
def salvar_item():
    produto = request.form["produto"]
    local = request.form["local"]
    data = request.form.get("data")
    descricao = request.form["descricao"]

    # Mantém a ordem esperada pelo model: item, descricao, local, data
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
        
        # 1. Gera o token
        token_gerado = gerador_de_token.dumps(email, salt='recuperar-senha-salt')
        
        try:
            # 2. Salva o token no banco usando a função do seu grupo
            salvar_token_recuperacao(email, token_gerado)
            
            # 3. CRUCIAL: Monta o link manualmente de forma simples, sem usar url_for!
            link_recuperacao = f"http://127.0.0{token_gerado}"
            
            # 4. Configura o e-mail real
            msg = Message(
                subject="Localiza+ - Recuperação de Senha",
                recipients=[email]
            )
            msg.body = f"Olá!\n\nPara redefinir sua senha no Localiza+, clique no link:\n{link_recuperacao}"
            
            # 5. Envia o e-mail de verdade
            mail.send(msg)
            
            sucesso = "O link de recuperação foi enviado para o seu e-mail!"
        except Exception as e:
            print("\n❌ ERRO DETALHADO:", e, "\n")
            erro = "Ocorreu um erro ao processar a recuperação."

    return render_template('recuperar-senha.html', erro=erro, sucesso=sucesso)

@app.route("/nova-senha/<token>", methods=["GET", "POST"])
def pag_nova_senha(token):
    erro = None
    usuario_valido = verificar_token_valido(token)
    
    if not usuario_valido:
        return "<h3>❌ Link inválido!</h3>"
    
    if request.method == "POST":
        nova_senha = request.form.get("nova_senha")
        atualizar_senha_por_token(token, nova_senha)
        return redirect(url_for('pag_login_aluno'))

    return render_template('nova-senha.html', erro=erro, token=token)





if __name__ == "__main__":
    app.run(debug=True)