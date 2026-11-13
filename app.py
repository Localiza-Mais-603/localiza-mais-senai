import calendar
import os
import socket
from datetime import date, datetime, timedelta
from pathlib import Path
from mysql.connector.errors import IntegrityError

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from database.conexao import conectar
from model.cadastro import cadastrar_usuario, cadastrar_coor, existe_coordenador
from model.excluir_item import excluir_itens
from model.filtro import buscar_itens_filtrados
from model.login import (
    verificar_login_coor,
    verificar_login_usuario,
    salvar_token_recuperacao,
    verificar_token_valido,
    atualizar_senha_por_token
)
from model.cadastrar_itens import (
    cadastrar_item,
    registrar_item_perdido,
    listar_categorias,
    cadastrar_categoria,
    cadastrar_item_encontrado,
    listar_destinos,
    excluir_categoria
)
from model.listar_itens import listar_todos
from model.visualizar_perfil import buscar_usuario_por_email
from model.editar_item import atualizar_item_no_banco
from model.retirada_itens import registrar_retirada_bd, devolver_item_bd
from model.gerenciar import listar_todos_coordenadores, buscar_coor_por_cpf, atualizar_coor, deletar_coor


load_dotenv(Path(__file__).resolve().parent / ".env")

socket.setdefaulttimeout(15)

app = Flask(__name__)
app.secret_key = "chciclete"


# ===== CONFIGURAÇÃO DE E-MAIL =====

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'localizamaisararaquara@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (
    'Localiza+',
    'localizamaisararaquara@gmail.com'
)

mail = Mail(app)
gerador_de_token = URLSafeTimedSerializer(app.secret_key)


# ===== PRAZOS DE DESCARTE =====

PRAZO_DESCARTE_MESES = 6
PRAZO_MARMITA_DIAS = 7
PRAZO_REDUZIDO_DIAS = None
PRAZO_DESCARTE_DIAS = PRAZO_DESCARTE_MESES * 30


def somar_meses(data, meses):
    """Soma meses de calendário a uma data."""
    mes = data.month - 1 + meses
    ano = data.year + mes // 12
    mes = mes % 12 + 1

    ultimo_dia = calendar.monthrange(ano, mes)[1]

    return date(ano, mes, min(data.day, ultimo_dia))


def e_marmita(item, nomes_categorias):
    """Identifica marmitas pelo nome, descrição ou categoria."""

    nome_categoria = nomes_categorias.get(
        str(item.get('id_categoria')), ''
    )

    texto = (
        f"{item.get('item') or ''} "
        f"{item.get('descricao') or ''} "
        f"{nome_categoria}"
    ).lower()

    return 'marmit' in texto


def calcular_prazo(item, eh_marmita=False):
    """Calcula o prazo de descarte do item."""

    data = item.get('data_encontrado')

    if isinstance(data, datetime):
        data = data.date()

    elif isinstance(data, str) and data:
        try:
            data = datetime.strptime(
                data[:10], '%Y-%m-%d'
            ).date()
        except ValueError:
            data = None

    if not data:
        item['prazo_texto'] = ''
        item['prazo_classe'] = ''
        item['prazo_resumo'] = ''
        return

    if eh_marmita:
        limite = data + timedelta(days=PRAZO_MARMITA_DIAS)
    else:
        limite = somar_meses(data, PRAZO_DESCARTE_MESES)

    if PRAZO_REDUZIDO_DIAS:
        limite = min(
            limite,
            data + timedelta(days=PRAZO_REDUZIDO_DIAS)
        )

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
            texto = f'Descarte em {dias} dias'
            restante = f'{dias} dias restantes'

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
    """Retorna o status em letras minúsculas."""

    return (item.get('status') or '').strip().lower()


def somente_numeros(texto):
    """Remove caracteres que não sejam números."""

    return ''.join(
        c for c in (texto or '') if c.isdigit()
    )


# ===== LOGIN E CADASTRO =====

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

    return render_template(
        "login.html",
        erro=erro,
        tipo='usuario',
        sucesso=sucesso
    )


@app.route("/login/setor/de/apoio", methods=["GET", "POST"])
def pag_login_coordenacao():

    erro = None
    ja_tem_coor = existe_coordenador()

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

    return render_template(
        "login.html",
        erro=erro,
        tipo='apoio',
        ja_tem_coor=ja_tem_coor
    )


@app.route("/cadastro/usuario")
def pag_cadastro():
    return render_template("cadastrar_usuario.html")


@app.route("/cadastro", methods=["POST"])
def cadastro():
    cpf = somente_numeros(request.form["CPF"])
    nome = request.form["nome_completo"].strip()
    curso = request.form["curso"]
    email = request.form["email"].strip()
    senha = request.form["senha"]

    try:
        cadastrar_usuario(cpf, nome, curso, email, senha)
    except IntegrityError:
        flash("CPF ou e-mail já cadastrado.", "danger")
        return redirect("/cadastro")

    return redirect("/login/usuario")


@app.route('/cadastro-coor', methods=['GET', 'POST'])
def cadastro_coor():
    ja_tem_coor = existe_coordenador()

    if ja_tem_coor and session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    if request.method == 'POST':
        nome = request.form['nome_completo'].strip()
        cpf = somente_numeros(request.form['cpf'])
        email = request.form['email'].strip()
        senha = request.form['senha']

        try:
            cadastrar_coor(nome, cpf, email, senha)
        except IntegrityError:
            flash("Já existe um coordenador cadastrado com este CPF ou e-mail.", "danger")
            return redirect(url_for('cadastro_coor'))

        if not ja_tem_coor:
            flash("Coordenador principal cadastrado com sucesso! Faça seu login.", "success")
            return redirect(url_for('pag_login_coordenacao'))
        else:
            flash("Novo coordenador cadastrado com sucesso!", "success")
            return redirect(url_for('gerenciar_coordenadores'))

    return render_template(
        'cadastro_coordenacao.html',
        primeiro_cadastro=not ja_tem_coor
    )


@app.route('/gerenciar-coordenadores')
def gerenciar_coordenadores():
    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    coordenadores = listar_todos_coordenadores()
    return render_template('gerenciamento_coor.html', coordenadores=coordenadores)


@app.route('/editar-coor/<cpf>', methods=['GET', 'POST'])
def editar_coor(cpf):
    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    cpf = somente_numeros(cpf)

    if request.method == 'POST':
        nome = request.form['nome_completo']
        email = request.form['email']
        nova_senha = request.form.get('senha')

        try:
            atualizar_coor(cpf, nome, email, nova_senha)
            flash("Dados do coordenador atualizados com sucesso!", "success")
            return redirect(url_for('gerenciar_coordenadores'))
        except IntegrityError:
            flash("Este e-mail já está em uso por outro coordenador.", "danger")
            return redirect(url_for('editar_coor', cpf=cpf))

    coordenador = buscar_coor_por_cpf(cpf)
    if not coordenador:
        flash("Coordenador não encontrado.", "danger")
        return redirect(url_for('gerenciar_coordenadores'))

    return render_template('editar_coordenacao.html', coordenador=coordenador)


@app.route('/remover-coor/<cpf>', methods=['POST'])
def remover_coor(cpf):
    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    cpf = somente_numeros(cpf)
    cpf_logado = somente_numeros(session.get("cpf", ""))

    if cpf_logado == cpf:
        flash("Você não pode remover o seu próprio usuário enquanto está logado.", "danger")
        return redirect(url_for('gerenciar_coordenadores'))

    if deletar_coor(cpf):
        flash("Coordenador removido com sucesso! Os itens vinculados foram mantidos.", "success")
    else:
        flash("Coordenador não encontrado ou já removido.", "danger")

    return redirect(url_for('gerenciar_coordenadores'))


@app.route("/editar-item-cadastrado")
def pag_editar_item_cadastrado():
    return render_template("editar-item-cadastrado.html")


@app.route("/visualizar-perfil")
def visualizar_perfil():

    usuario_sessao = session.get("usuario")

    if not usuario_sessao:
        return redirect(url_for("pag_login_aluno"))

    email = (
        usuario_sessao.get("email")
        if isinstance(usuario_sessao, dict)
        else usuario_sessao[0]
    )

    usuario_atualizado = buscar_usuario_por_email(email)

    return render_template(
        "visualizar_perfil.html",
        usuario=usuario_atualizado
    )


@app.route


# ===== VISUALIZAR ITENS =====

@app.route("/visualizar-itens", methods=["GET"])
def visualizar_itens():

    usuario_sessao = session.get("usuario")
    perfil = session.get("perfil")
    usuario_atualizado = None

    if usuario_sessao:

        email = (
            usuario_sessao.get("email")
            if isinstance(usuario_sessao, dict)
            else usuario_sessao[0]
        )

        if perfil == "coordenacao":

            conexao, cursor = conectar()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM coordenador WHERE email = %s",
                (email,)
            )

            usuario_atualizado = cursor.fetchone()

            cursor.close()
            conexao.close()

        else:
            usuario_atualizado = buscar_usuario_por_email(email)

    categorias_ids = request.args.getlist("categoria")
    apenas_disponiveis = request.args.get("disponivel")

    categorias_ids = [
        c for c in categorias_ids if c.strip()
    ]

    if categorias_ids or apenas_disponiveis:
        itens = buscar_itens_filtrados(
            categorias_ids,
            apenas_disponiveis
        )
    else:
        itens = listar_todos()

    # Esconde arquivados, perdidos e retirados da tela principal.

    itens = [
        item for item in itens
        if status_do_item(item) not in (
            'arquivado',
            'perdido',
            'retirado'
        )
    ]

    categorias = listar_categorias()
    destinos = listar_destinos()

    # Mapa de ID para nome da categoria.

    nomes_categorias = {}

    for cat in categorias:

        cat_id = (
            cat.get('id_categoria', cat.get('id'))
            if isinstance(cat, dict)
            else cat[0]
        )

        cat_nome = (
            cat.get('nome')
            if isinstance(cat, dict)
            else cat[1]
        )

        nomes_categorias[str(cat_id)] = cat_nome or ''

    for item in itens:

        email_publicador = item.get('email')

        if email_publicador:

            publicador = buscar_usuario_por_email(
                email_publicador
            )

            item['publicado_nome'] = (
                publicador['nome'] if publicador else ''
            )

        else:
            item['publicado_nome'] = ''

        calcular_prazo(
            item,
            e_marmita(item, nomes_categorias)
        )

    return render_template(
        "visualizar_itens.html",
        itens=itens,
        usuario=usuario_atualizado,
        categorias=categorias,
        destinos=destinos,
        prazo_dias=PRAZO_DESCARTE_DIAS,
        prazo_meses=PRAZO_DESCARTE_MESES,
        prazo_marmita_dias=PRAZO_MARMITA_DIAS,
        prazo_reduzido_dias=PRAZO_REDUZIDO_DIAS
    )


# ===== CADASTRO DE ITEM PELA COORDENAÇÃO =====

@app.route("/cadastrar/item/salvar", methods=["POST"])
def registrar_itens_coordenacao():

    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    item = request.form.get("item")

    id_categoria = request.form.get("id_categoria")

    id_categoria = (
        int(id_categoria)
        if id_categoria and id_categoria.strip()
        else None
    )

    data_encontrado = request.form.get("data")

    if not data_encontrado or not data_encontrado.strip():
        data_encontrado = date.today().strftime('%Y-%m-%d')

    nome_foto = None
    foto = request.files.get("foto")

    if foto and foto.filename != "":

        nome_seguro = secure_filename(foto.filename)

        prefixo = datetime.now().strftime(
            "%Y%m%d%H%M%S_"
        )

        nome_foto = prefixo + nome_seguro

        pasta_destino = os.path.join(
            "static",
            "img_upload"
        )

        os.makedirs(pasta_destino, exist_ok=True)

        foto.save(
            os.path.join(pasta_destino, nome_foto)
        )

    cpf_coordenador = session.get(
        "usuario", {}
    ).get("cpf")

    cadastrar_item(
        item=item,
        descricao="",
        data_encontrado=data_encontrado,
        status="DISPONIVEL",
        id_categoria=id_categoria,
        local=None,
        foto=nome_foto,
        email=None,
        cpf_coordenador=cpf_coordenador
    )

    flash("Item cadastrado com sucesso!", "success")

    return redirect(url_for("visualizar_itens"))


# ===== PERDI ALGO =====

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

            pasta_destino = os.path.join(
                "static",
                "img_upload"
            )

            os.makedirs(pasta_destino, exist_ok=True)

            caminho_completo = os.path.join(
                pasta_destino,
                nome_foto
            )

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

        flash(
            "Seu relato foi enviado à coordenação!",
            "success"
        )

        return redirect(url_for("visualizar_itens"))

    categorias = listar_categorias()

    return render_template(
        "registrar_item_perdido.html",
        categorias=categorias
    )


# ===== ENCONTREI ALGO =====

@app.route("/registro/itens/encontrado", methods=["POST"])
def registrar_item_encontrado():

    if session.get("perfil") != "aluno":
        return redirect(url_for("pag_login_aluno"))

    item = request.form.get("item")
    descricao = request.form.get("descricao")
    id_categoria = int(request.form.get("id_categoria"))
    local = request.form.get("local")
    data_encontrado = request.form.get("data")

    destino_objeto = request.form.get("destino")

    if destino_objeto == "outro":
        destino_objeto = (
            "Outro: " +
            request.form.get("destino_outro", "")
        )

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

    flash(
        f"Achado publicado! Publicado por {usuario['nome']} ({usuario['email']})",
        "success"
    )

    return redirect(url_for("visualizar_itens"))


# ===== CATEGORIAS =====

@app.route("/api/categorias", methods=["POST"])
def api_cadastrar_categoria():

    dados = request.get_json()
    nome = dados.get("nome") if dados else None

    if not nome or nome.strip() == "":
        return jsonify({
            "sucesso": False,
            "mensagem": "Nome da categoria inválido."
        }), 400

    id_novo = cadastrar_categoria(nome.strip())

    return jsonify({
        "sucesso": True,
        "id_categoria": id_novo,
        "nome": nome.strip()
    })


@app.route("/excluir-categoria/<int:id_categoria>", methods=["POST"])
def excluir_categoria_rota(id_categoria):

    if session.get("perfil") != "coordenacao":
        return redirect("/login/usuario")

    excluir_categoria(id_categoria)

    flash("Categoria excluída com sucesso!", "success")

    return redirect(url_for("visualizar_itens"))


# ===== RECUPERAÇÃO DE SENHA =====

@app.route("/recuperar-senha", methods=["GET", "POST"])
def pag_recuperar_senha():

    erro = None
    sucesso = None

    if request.method == "POST":

        email = request.form.get("email")

        token_gerado = gerador_de_token.dumps(
            email,
            salt='recuperar-senha-salt'
        )

        try:

            salvar_token_recuperacao(
                email,
                token_gerado
            )

            link_recuperacao = url_for(
                'pag_nova_senha',
                token=token_gerado,
                _external=True
            )

            msg = Message(
                subject="Localiza+ - Recuperação de Senha",
                recipients=[email]
            )

            msg.body = (
                f"Olá!\n\n"
                f"Para redefinir sua senha no Localiza+, "
                f"clique no link abaixo:\n\n"
                f"{link_recuperacao}\n\n"
                f"Se você não solicitou essa alteração, "
                f"ignore este e-mail."
            )

            mail.send(msg)

            sucesso = "E-mail enviado!"

        except ValueError as e_validacao:
            erro = str(e_validacao)

        except Exception as e:
            print("\nERRO DETALHADO NO ENVIO:", e, "\n")
            erro = "Ocorreu um erro ao processar a recuperação de senha."

    return render_template(
        'recuperar-senha.html',
        erro=erro,
        sucesso=sucesso
    )


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

            return render_template(
                'nova-senha.html',
                erro=erro,
                token=token
            )

        atualizar_senha_por_token(
            token,
            nova_senha
        )

        return redirect(
            url_for(
                'pag_login_aluno',
                sucesso="Senha alterada com sucesso! Faça seu login."
            )
        )

    return render_template(
        'nova-senha.html',
        erro=erro,
        token=token
    )


# ===== EXCLUIR ITEM =====

@app.route('/excluir-item/<int:id_item>', methods=['POST'])
def excluir_item(id_item):

    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    excluir_itens(id_item)

    return redirect(request.referrer or '/')


# ===== ARQUIVAR ITEM =====

@app.route('/arquivar-item/<int:id_item>', methods=['POST'])
def arquivar_item(id_item):

    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    try:
        from model.editar_item import atualizar_status_item

        atualizar_status_item(
            id_item,
            'Arquivado'
        )

    except Exception as e:
        print("Erro ao arquivar item:", e)

    return redirect(url_for('itens_arquivados'))


# ===== ITENS ARQUIVADOS =====

@app.route("/itens-arquivados")
def itens_arquivados():

    if session.get('perfil') != 'coordenacao':
        return redirect(url_for('pag_login_aluno'))

    usuario_sessao = session.get("usuario")
    usuario_atualizado = None

    if usuario_sessao:

        email = (
            usuario_sessao.get("email")
            if isinstance(usuario_sessao, dict)
            else usuario_sessao[0]
        )

        usuario_atualizado = buscar_usuario_por_email(email)

    todos_itens = listar_todos()

    arquivados = [
        item for item in todos_itens
        if status_do_item(item) == 'arquivado'
    ]

    return render_template(
        "arquivar_itens_coor.html",
        itens=arquivados,
        usuario=usuario_atualizado
    )


# ===== DESARQUIVAR ITEM =====

@app.route('/desarquivar-item/<int:id_item>', methods=['POST'])
def desarquivar_item(id_item):

    if session.get('perfil') != 'coordenacao':
        return redirect('/login/usuario')

    try:
        from model.editar_item import atualizar_status_item

        atualizar_status_item(
            id_item,
            'DISPONIVEL'
        )

    except Exception as e:
        print("Erro ao desarquivar item:", e)

    return redirect(url_for('visualizar_itens'))


# ===== RELATÓRIOS DE PERDA =====

@app.route("/relatorios-perda")
def relatorios_perda():

    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    usuario_sessao = session.get("usuario")
    usuario_atualizado = None

    if usuario_sessao:

        email = (
            usuario_sessao.get("email")
            if isinstance(usuario_sessao, dict)
            else usuario_sessao[0]
        )

        usuario_atualizado = buscar_usuario_por_email(email)

    todos_itens = listar_todos()

    itens_relatados = [
        item for item in todos_itens
        if status_do_item(item) == 'perdido'
    ]

    for item in itens_relatados:

        email_publicador = item.get('email')

        if email_publicador:

            publicador = buscar_usuario_por_email(
                email_publicador
            )

            item['publicado_nome'] = (
                publicador['nome'] if publicador else ''
            )

        else:
            item['publicado_nome'] = ''

    return render_template(
        "relatorios_perda.html",
        itens=itens_relatados,
        usuario=usuario_atualizado
    )


# ===== EDITAR ITEM =====

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

    atualizar_item_no_banco(
        id_item,
        item_nome,
        descricao,
        local,
        data_encontrado
    )

    return redirect(url_for("visualizar_itens"))


# ===== MEU HISTÓRICO =====

@app.route("/meu-historico")
def meu_historico():

    if session.get("perfil") != "aluno":
        return redirect(url_for("pag_login_aluno"))

    usuario_sessao = session.get("usuario")

    email = (
        usuario_sessao.get("email")
        if isinstance(usuario_sessao, dict)
        else usuario_sessao[0]
    )

    usuario_atualizado = buscar_usuario_por_email(email)

    todos_itens = listar_todos()

    meus_itens = [
        item for item in todos_itens
        if (
            item.get("email")
            if isinstance(item, dict)
            else getattr(item, "email", None)
        ) == email
    ]

    return render_template(
        "historico_usuario.html",
        itens=meus_itens,
        usuario=usuario_atualizado
    )


# ===== RETIRAR ITEM =====

@app.route("/retirar-item", methods=["POST"])
def retirar_item():

    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_aluno"))

    id_item = request.form.get("id_item")
    nome_retirante = request.form.get("nome_retirante")
    email_retirante = request.form.get("email_retirante")

    try:

        registrar_retirada_bd(
            id_item,
            nome_retirante,
            email_retirante
        )

        flash(
            f"Item retirado por {nome_retirante} com sucesso!",
            "success"
        )

    except Exception as e:

        print("Erro ao registrar retirada:", e)

        flash(
            "Erro ao registrar retirada do item.",
            "error"
        )

    return redirect(url_for("itens_retirados"))


# ===== REIVINDICAR ITEM =====

@app.route("/reivindicar-item/<int:id_item>", methods=["POST"])
def reivindicar_item(id_item):

    if session.get("perfil") != "aluno":
        return redirect(url_for("pag_login_aluno"))

    usuario_sessao = session.get("usuario")

    email_aluno = (
        usuario_sessao.get("email")
        if isinstance(usuario_sessao, dict)
        else usuario_sessao[0]
    )

    aluno = buscar_usuario_por_email(email_aluno)

    item = next(
        (
            i for i in listar_todos()
            if i.get("id_item") == id_item
        ),
        None
    )

    if not aluno or not item:

        flash(
            "Não foi possível localizar o item.",
            "error"
        )

        return redirect(url_for("visualizar_itens"))

    email_coordenacao = os.getenv(
        "EMAIL_COORDENACAO",
        "giovannacarraro436@gmail.com"
    )

    destinatarios = [email_coordenacao]

    data = item.get("data_encontrado")

    data_txt = (
        data.strftime("%d/%m/%Y")
        if hasattr(data, "strftime")
        else (data or "não informada")
    )

    try:

        msg = Message(
            subject=f"Localiza+ - Solicitação de item: {item['item']}",
            recipients=destinatarios,
            reply_to=aluno["email"]
        )

        msg.body = (
            f"Olá, coordenação!\n\n"
            f"O aluno {aluno['nome']} (e-mail: {aluno['email']}"
            f"{', curso: ' + aluno['curso'] if aluno.get('curso') else ''}) "
            f"informou que o item abaixo é dele e solicitou a retirada.\n\n"
            f"Item: {item['item']}\n"
            f"Descrição: {item.get('descricao') or 'não informada'}\n"
            f"Local: {item.get('local') or 'não informado'}\n"
            f"Data: {data_txt}\n\n"
            f"Entre em contato com o aluno para confirmar que o item é dele e combinar a retirada.\n\n"
            f"-- Sistema Localiza+"
        )

        mail.send(msg)

        flash(
            "Solicitação enviada! A coordenação entrará em contato com você.",
            "success"
        )

    except Exception:

        import traceback
        traceback.print_exc()

        flash(
            "Não foi possível enviar a solicitação agora. Tente novamente.",
            "error"
        )

    return redirect(url_for("visualizar_itens"))


# ===== ITENS RETIRADOS =====

@app.route("/itens_retirados")
def itens_retirados():

    if session.get('perfil') != 'coordenacao':
        return redirect(url_for('pag_login_aluno'))

    usuario_sessao = session.get("usuario")
    usuario_atualizado = None

    if usuario_sessao:

        email = (
            usuario_sessao.get("email")
            if isinstance(usuario_sessao, dict)
            else usuario_sessao[0]
        )

        usuario_atualizado = buscar_usuario_por_email(email)

    todos_itens = listar_todos()

    retirados = [
        item for item in todos_itens
        if status_do_item(item) == 'retirado'
    ]

    for item in retirados:

        dt_ret = item.get('data_retirada')

        if isinstance(dt_ret, datetime):

            item['data_retirada_fmt'] = dt_ret.strftime(
                '%d/%m/%Y às %H:%M'
            )

        elif isinstance(dt_ret, str) and dt_ret:

            item['data_retirada_fmt'] = dt_ret

        else:

            item['data_retirada_fmt'] = 'Não informada'

    return render_template(
        "itens_retirados.html",
        itens=retirados,
        usuario=usuario_atualizado
    )


# ===== DEVOLVER ITEM =====

@app.route("/devolver-item/<int:id_item>", methods=["POST"])
def devolver_item(id_item):

    if session.get("perfil") != "coordenacao":
        return redirect(url_for("pag_login_coordenacao"))

    try:

        devolver_item_bd(id_item)

        flash(
            "Item devolvido para a lista de disponíveis com sucesso!",
            "success"
        )

    except Exception as e:

        print("Erro ao devolver item:", e)

        flash(
            "Erro ao devolver o item.",
            "error"
        )

    return redirect(url_for("itens_retirados"))


# ===== EXCLUIR MEU RELATO =====

@app.route('/excluir-meu-relato/<int:id_item>', methods=['POST'])
def excluir_meu_relato(id_item):

    if session.get('perfil') != 'aluno':
        return redirect(url_for('pag_login_aluno'))

    usuario_sessao = session.get("usuario")

    email_logado = (
        usuario_sessao.get("email")
        if isinstance(usuario_sessao, dict)
        else usuario_sessao[0]
    )

    todos_itens = listar_todos()

    item_pertence_ao_usuario = any(
        item.get("id_item") == id_item
        and item.get("email") == email_logado
        for item in todos_itens
    )

    if item_pertence_ao_usuario:

        excluir_itens(id_item)

        flash(
            "Relato excluído com sucesso!",
            "success"
        )

    else:

        flash(
            "Você não tem permissão para excluir este relato.",
            "error"
        )

    return redirect(url_for('meu_historico'))


# ===== INICIAR SERVIDOR =====

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8080
    )