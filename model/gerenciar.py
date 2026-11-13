from contextlib import contextmanager
from werkzeug.security import generate_password_hash
from database.conexao import conectar


@contextmanager
def _cursor(dictionary=False, commit=False):
    """
    Abre conexão + cursor e garante o fechamento, mesmo se der erro.
    Em caso de exceção faz rollback e repassa o erro para a rota tratar.
    """
    conexao, cursor_padrao = conectar()
    cursor_padrao.close()

    cursor = conexao.cursor(dictionary=dictionary)

    try:
        yield cursor

        if commit:
            conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


def listar_todos_coordenadores():
    with _cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT cpf, nome, email FROM coordenador ORDER BY nome ASC"
        )
        return cursor.fetchall()


def buscar_coor_por_cpf(cpf):
    with _cursor(dictionary=True) as cursor:
        cursor.execute(
            "SELECT cpf, nome, email FROM coordenador WHERE cpf = %s",
            (cpf,)
        )
        return cursor.fetchone()


def atualizar_coor(cpf, nome, email, nova_senha=None):
    """Atualiza nome/e-mail. Só troca a senha se nova_senha não estiver vazia."""
    with _cursor(commit=True) as cursor:
        if nova_senha and nova_senha.strip():
            cursor.execute(
                "UPDATE coordenador SET nome = %s, email = %s, senha = %s "
                "WHERE cpf = %s",
                (nome.strip(), email.strip(), generate_password_hash(nova_senha), cpf)
            )
        else:
            cursor.execute(
                "UPDATE coordenador SET nome = %s, email = %s WHERE cpf = %s",
                (nome.strip(), email.strip(), cpf)
            )


def deletar_coor(cpf):
    """Desvincula os itens do coordenador e depois o remove."""
    with _cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE item SET cpf_coordenador = NULL WHERE cpf_coordenador = %s",
            (cpf,)
        )
        cursor.execute("DELETE FROM coordenador WHERE cpf = %s", (cpf,))
        return cursor.rowcount > 0