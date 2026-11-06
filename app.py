from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from database.conexao import conectar
from model.cadastro import cadastrar_usuario, cadastrar_coor
from model.excluir_item import excluir_itens
from model.filtro import buscar_itens_filtrados
from model.login import verificar_login_coor, verificar_login_usuario, salvar_token_recuperacao, verificar_token_valido, atualizar_senha_por_token
from dotenv import load_dotenv
from model.cadastrar_itens import cadastrar_item, registrar_item_perdido, listar_categorias, cadastrar_categoria, cadastrar_item_encontrado, listar_destinos, excluir_categoria
from model.listar_itens import listar_todos
from model.visualizar_perfil import buscar_usuario_por_email
from model.editar_item import atualizar_item_no_banco
import os
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = "chciclete"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'localizamaisararaquara@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Localiza+', 'localizamaisararaquara@gmail.com')

mail = Mail(app)
gerador_de_token = URLSafeTimedSerializer(app.secret_key)



# Prazo (em dias) para retirada do item antes do descarte. Altere aqui se precisar.
PRAZO_DESCARTE_DIAS = 90


def calcular_prazo(item):
    """Calcula o prazo de descarte do item a partir da data em que foi encontrado."""
    data = item.get('data_encontrado')

    if isinstance(data, datetime):
        data = data.date()
    elif isinstance(data, str) and data:
        try:
            data = datetime.strptime(data[:10], '%Y-%m-%d').date()
        except ValueError:
            data = None

    if not data:
        item['prazo_texto'] = ''
        item['prazo_classe'] = ''
        item['prazo_resumo'] = ''
        return

    limite = data + timedelta(days=PRAZO_DESCARTE_DIAS)
    dias = (limite - date.today()).days
    limite_txt = limite.strftime('%d/%m/%Y')

    if dias < 0:
        texto = 'Prazo encerrado'
        classe = 'prazo-vencido'
        resumo = f'encerrado em {limite_txt}'
    else:
        if dias == 0:
            texto, restante = 'Descarte hoje', 'último dia'
        elif dias == 1:
            texto, restante = 'Descarte amanhã', '1 dia restante'
        else:
            texto, restante = f'Descarte em {dias} dias', f'{dias} dias restantes'

        if dias <= 7:
            classe = 'prazo-urgente'
        elif dias <= 30:
            classe = 'prazo-atencao'
        else:
            classe = 'prazo-ok'
        resumo = f'até {limite_txt} ({restante})'

    item['prazo_texto'] = texto
    item['prazo_classe'] = classe
    item['prazo_resumo'] = resumo


def status_do_item(item):
    """Devolve o status do item em minúsculas, sem espaços (evita erro de maiúscula/minúscula)."""
    return (item.get('status') or '').strip().lower()


def somente_numeros(texto):
    """Remove pontos, traços e espaços (o CPF no banco tem só 11 números)."""
    return ''.join(c for c in (texto or '') if c.isdigit())


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
        cpf = somente_numeros(request.form["cpf"])
        senha = request.form["senha"]
        coordenador = verificar_login_coor(cpf, senha)
        if coordenador:
            session["usuario"] = coordenador
            session["perfil"] = "coordenacao"
            return redirect(url_for("visualizar_itens"))
        else:
            erro = "CPF ou senha incorretos!"
    return render_template("login.html", erro=erro, tipo='apoio')

@app.route("/cadastro/usuario")
def pag_cadastro():
    return render_template("cadastrar_usuario.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    cpf = somente_numeros(request.form["CPF"])
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
        cpf = somente_numeros(request.form['cpf'])
        email = request.form['email']
        senha = request.form['senha']
        cadastrar_coor(nome, cpf, email, senha)
        return redirect('/login/setor/de/apoio')
    return render_template('cadastro_coordenacao.html')

@app.route("/editar-item-cadastrado")
def pag_editar_item_cadastrado():
    return render_template("editar-item-cadastrado.html")

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

    # Esconde da tela principal: arquivados e relatos de perda (só a coordenação vê, em Relatórios)
    itens = [
        item for item in itens
        if status_do_item(item) not in ('arquivado', 'perdido')
    ]

    for item in itens:
        # Nome de quem publicou o item
        email_publicador = item.get('email')
        if email_publicador:
            publicador = buscar_usuario_por_email(email_publicador)
            item['publicado_nome'] = publicador['nome'] if publicador else ''
        else:
            item['publicado_nome'] = ''

        # Prazo de retirada / descarte
        calcular_prazo(item)

    categorias = listar_categorias()
    destinos = listar_destinos()

    return render_template(
        "visualizar_itens.html",
        itens=itens,
        usuario=usuario_atualizado,
        categorias=categorias,
        destinos=destinos,
        prazo_dias=PRAZO_DESCARTE_DIAS
    )

@app.route("/adicionar/item")
def pag_cadastrar_item_coor():
    categorias_bd = listar_categorias()
    return render_template("cadastrar_itens_coor.html", categorias=categorias_bd)


@app.route("/cadastrar/item/salvar", methods=["POST"])
def registrar_itens_coordenacao():
    item = request.form.get("item")

    # Tratamento da categoria
    id_categoria = request.form.get("id_categoria")
    id_categoria = int(id_categoria) if id_categoria and id_categoria.strip() else None

    local = request.form.get("local")

    # Tratamento da data
    data_encontrado = request.form.get("data")
    if not data_encontrado or not data_encontrado.strip():
        data_encontrado = None

    descricao = request.form.get("descricao")
    cpf_coordenador = session.get("usuario", {}).get("cpf")

    cadastrar_item(
        item=item,
        descricao=descricao,
        data_encontrado=data_encontrado,
        status="DISPONIVEL",
        id_categoria=id_categoria,
        local=local,
        foto=None,
        email=None,
        cpf_coordenador=cpf_coordenador
    )

    return redirect(url_for("visualizar_itens"))


# PERDI ALGO: o aluno relata a perda e o relato vai só para a coordenação (aba Relatórios)
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

        flash("Seu relato foi enviado à coordenação!", "success")

        return redirect(url_for("visualizar_itens"))

    categorias = listar_categorias()
    return render_template("registrar_item_perdido.html", categorias=categorias)


# ENCONTREI ALGO: o aluno cadastra o item achado e ele aparece na lista principal
@app.route("/registro/itens/encontrado", methods=["POST"])
def registrar_item_encontrado():
    if session.get("perfil") != "aluno":
        return redirect(url_for("pag_login_aluno"))

    item = request.form.get("item")
    descricao = request.form.get("descricao")
    id_categoria = int(request.form.get("id_categoria"))
    local = request.form.get("local")
    data_encontrado = request.form.get("data")

    # o que a pessoa fez com o objeto -> coluna destino_objeto
    destino_objeto = request.form.get("destino")
    if destino_objeto == "outro":
        destino_objeto = "Outro: " + request.form.get("destino_outro", "")

    email = session["usuario"].get("email")

    cadastrar_item_encontrado(
        item=item,
        descricao=descricao,
        data_encontrado=data_encontrado,
        id_categoria=id_categoria,
        local=local,
        email=email,
        destino_objeto=destino_objeto
    )

    usuario = buscar_usuario_por_email(email)
    flash(f"Achado publicado! Publicado por {usuario['nome']} ({usuario['email']})", "success")
    return redirect(url_for("visualizar_itens"))


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


# Só a coordenação pode excluir categorias (os itens ficam sem categoria)
@app.route("/excluir-categoria/<int:id_categoria>", methods=["POST"])
def excluir_categoria_rota(id_categoria):
    if session.get("perfil") != "coordenacao":
        return redirect("/login/usuario")

    excluir_categoria(id_categoria)
    flash("Categoria excluída com sucesso!", "success")
    return redirect(url_for("visualizar_itens"))


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


@app.route('/arquivar-item/<int:id_item>', methods=['POST'])
def arquivar_item(id_item):
    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    try:
        from model.editar_item import atualizar_status_item
        atualizar_status_item(id_item, 'Arquivado')
    except Exception as e:
        print("Erro ao arquivar item:", e)

    # Redireciona diretamente para a tela de itens arquivados
    return redirect(url_for('itens_arquivados'))

@app.route("/itens-arquivados")
def itens_arquivados():
    if session.get('perfil') != 'coordenacao':
        return redirect(url_for('pag_login_aluno'))

    usuario_sessao = session.get("usuario")
    usuario_atualizado = None
    if usuario_sessao:
        email = usuario_sessao.get("email") if isinstance(usuario_sessao, dict) else usuario_sessao[0]
        usuario_atualizado = buscar_usuario_por_email(email)

    todos_itens = listar_todos()
    arquivados = [item for item in todos_itens if status_do_item(item) == 'arquivado']

    return render_template("arquivar_itens_coor.html", itens=arquivados, usuario=usuario_atualizado)

@app.route('/desarquivar-item/<int:id_item>', methods=['POST'])
def desarquivar_item(id_item):
    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    try:
        from model.editar_item import atualizar_status_item
        # Define o status como 'DISPONIVEL' para aparecer na tela principal
        atualizar_status_item(id_item, 'DISPONIVEL')
    except Exception as e:
        print("Erro ao desarquivar item:", e)
    return redirect(url_for('visualizar_itens'))

@app.route("/relatorios-perda")
def relatorios_perda():
    # Proteção: apenas coordenação pode acessar
    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    usuario_sessao = session.get("usuario")
    usuario_atualizado = None
    if usuario_sessao:
        email = usuario_sessao.get("email") if isinstance(usuario_sessao, dict) else usuario_sessao[0]
        usuario_atualizado = buscar_usuario_por_email(email)

    # Apenas os relatos de "Perdi algo" (status Perdido)
    todos_itens = listar_todos()
    itens_relatados = [item for item in todos_itens if status_do_item(item) == 'perdido']

    # Nome de quem relatou a perda (disponível como item.publicado_nome no template)
    for item in itens_relatados:
        email_publicador = item.get('email')
        if email_publicador:
            publicador = buscar_usuario_por_email(email_publicador)
            item['publicado_nome'] = publicador['nome'] if publicador else ''
        else:
            item['publicado_nome'] = ''

    return render_template(
        "relatorios_perda.html",
        itens=itens_relatados,
        usuario=usuario_atualizado
    )

@app.route("/atualizar-item/<int:id_item>", methods=["POST"])
def editar_item(id_item):
    if session.get('perfil') != 'coordenacao':
        return redirect(url_for('pag_login_aluno'))

    item_nome = request.form.get("item")
    descricao = request.form.get("descricao")
    local = request.form.get("local")
    data_encontrado = request.form.get("data")
    if data_encontrado == "":
        data_encontrado = None

    # Atualiza no banco sem alterar o status
    atualizar_item_no_banco(id_item, item_nome, descricao, local, data_encontrado)

    return redirect(url_for("visualizar_itens"))

@app.route('/solicitar_item/<int:id_item>', methods=['POST'])
def solicitar_item(id_item):
    usuario_sessao = session.get("usuario")
    if not usuario_sessao or session.get('perfil') != 'aluno':
        flash('Faça login como aluno para solicitar um item.', 'warning')
        return redirect(url_for('pag_login_aluno'))
    
    id_aluno = usuario_sessao.get('id_usuario') if isinstance(usuario_sessao, dict) else usuario_sessao[0]
    
    try:
        conexao, cursor = conectar()
        
        cursor.execute("""
            UPDATE itens 
            SET aluno_reivindicante_id = %s 
            WHERE id_item = %s
        """, (id_aluno, id_item))
        
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Solicitação enviada com sucesso! Compareça à coordenação.', 'success')
    except Exception as e:
        print("Erro ao solicitar item:", e)
        flash('Ocorreu um erro ao processar sua solicitação.', 'danger')

    return redirect(url_for('visualizar_itens'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)