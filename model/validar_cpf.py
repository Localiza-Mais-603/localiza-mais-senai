def validar_cpf(cpf):
    # Remove caracteres não numéricos (pontos e traços)
    cpf = "".join([c for c in cpf if c.isdigit()])

    # Verifica se tem 11 dígitos ou se é uma sequência repetida conhecida
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Validação do 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(cpf[10]):
        return False

    return True