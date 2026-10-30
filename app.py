from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from database.conexao import conectar
from model.cadastro import cadastrar_usuario, cadastrar_coor
from model.excluir_item import excluir_itens
from model.filtro import buscar_itens_filtrados
from model.login import verificar_login_coor, verificar_login_usuario, salvar_token_recuperacao, verificar_token_valido, atualizar_senha_por_token
from dotenv import load_dotenv
from model.cadastrar_itens import cadastrar_item, registrar_item_perdido, listar_categorias, cadastrar_categoria
from model.listar_itens import listar_todos
from model.visualizar_perfil import buscar_usuario_por_email
from model.editar_item import atualizar_item_no_banco
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
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("perfil", None)
    return redirect("/")

@app.route("/login/usuario", methods=["GET", "POST"])
def pag_login_aluno():
    erro = None
    sucesso = request.args.get("sucesso") 
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = verificar_login_usuario(email, senha)
        if usuario:
            session["usuario"] = usuario 
            session["perfil"] = "aluno"  
            return redirect(url_for("visualizar_itens"))  
        else:
            erro = "E-mail ou senha incorretos!"
    return render_template("login.html", erro=erro, tipo='usuario')

@app.route("/login/setor/de/apoio", methods=["GET", "POST"])
def pag_login_coordenacao():
    erro = None
    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        coordenador = verificar_login_coor(cpf, senha)
        if coordenador:
            session["usuario"] = coordenador 
            session["perfil"] = "coordenacao"  
            return redirect(url_for("visualizar_itens"))  
        else:
            erro = "CPF ou senha incorretos!"
    return render_template("login.html", erro=erro, tipo = 'apoio' )

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

# ATUALIZAR ITEM NO BANCO (MODAL)
@app.route("/atualizar-item/<int:id_item>", methods=["POST"])
def atualizar_item_rota(id_item):
    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    item = request.form.get("item")
    descricao = request.form.get("descricao")
    local = request.form.get("local")
    data = request.form.get("data")
    status = request.form.get("status")
    
    foto = request.files.get("foto")
    nome_foto = None
    if foto and foto.filename != "":
        nome_foto = secure_filename(foto.filename)
        pasta_destino = os.path.join("static", "img_upload")
        os.makedirs(pasta_destino, exist_ok=True)
        foto.save(os.path.join(pasta_destino, nome_foto))

    atualizar_item_no_banco(id_item, item, descricao, local, data, status, nome_foto)
    flash("Item alterado com sucesso!", "success")

    return redirect(url_for('visualizar_itens'))

@app.route("/adicionar/item")
def pag_cadastrar_item_coor():
    return render_template("cadastrar_itens_coor.html")

@app.route("/visualizar-perfil")
def visualizar_perfil():
    usuario_sessao = session.get("usuario")
    if not usuario_sessao:
        return redirect(url_for("pag_login_aluno"))
    email = usuario_sessao.get("email") if isinstance(usuario_sessao, dict) else usuario_sessao[0]
    usuario_atualizado = buscar_usuario_por_email(email)
    return render_template("visualizar_perfil.html", usuario=usuario_atualizado)

@app.route("/visualizar-itens", methods=["GET"])
def visualizar_itens():
    usuario_sessao = session.get("usuario")
    perfil = session.get("perfil")
    usuario_atualizado = None

    if usuario_sessao:
        email = usuario_sessao.get("email") if isinstance(usuario_sessao, dict) else usuario_sessao[0]
        
        if perfil == "coordenacao":
            conexao, cursor = conectar()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM coordenador WHERE email = %s", (email,))
            usuario_atualizado = cursor.fetchone()
            cursor.close()
            conexao.close()
        else:
            usuario_atualizado = buscar_usuario_por_email(email)

    categorias_ids = request.args.getlist("categoria")
    apenas_disponiveis = request.args.get("disponivel")
    categorias_ids = [c for c in categorias_ids if c.strip()]
    
    if categorias_ids or apenas_disponiveis:
        itens = buscar_itens_filtrados(categorias_ids, apenas_disponiveis)
    else:
        itens = listar_todos()
        
    categorias = listar_categorias()
    
    return render_template(
        "visualizar_itens.html", 
        itens=itens, 
        usuario=usuario_atualizado, 
        categorias=categorias
    )

@app.route("/registro/itens", methods=["GET", "POST"])
def registrar_itens():
    if request.method == "POST":
        item = request.form.get("item")
        id_categoria = request.form.get("categoria_id")
        if not id_categoria or id_categoria.strip() == "":
            id_categoria = None
        else:
            id_categoria = int(id_categoria)
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
            id_categoria=id_categoria,
            local=local,
            foto=nome_foto,
            email=email,
            cpf_coordenador=None
        )
        return redirect(url_for("registrar_itens"))
        
    categorias = listar_categorias()
    return render_template("registrar_item_perdido.html", categorias=categorias)

@app.route("/api/categorias", methods=["POST"])
def api_cadastrar_categoria():
    dados = request.get_json()
    nome = dados.get("nome") if dados else None
    if not nome or nome.strip() == "":
        return jsonify({"sucesso": False, "mensagem": "Nome da categoria inválido."}), 400
    id_novo = cadastrar_categoria(nome.strip())
    return jsonify({
        "sucesso": True, 
        "id_categoria": id_novo, 
        "nome": nome.strip()
    })

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
            sucesso = "E-mail enviado!"
        except ValueError as e_validacao:
            erro = str(e_validacao)
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
        return redirect(url_for('pag_login_aluno', sucesso="Senha alterada com sucesso! Faça seu login."))
    return render_template('nova-senha.html', erro=erro, token=token)

@app.route('/excluir-item/<int:id_item>', methods=['POST'])
def excluir_item(id_item):
    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')
    excluir_itens(id_item)
    return redirect(request.referrer or '/')

if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port= 8080)