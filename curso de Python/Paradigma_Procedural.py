def menu():
    print(f''' Seja bem vindo!!!
    #########menu#########
    1 deposito
    2 saque
    3 extrato
    4 criar usuario
    5 criar conta
    6 listar contas
    0 sair''')
    return int(input(f''' Qual é sua opcao?\n '''))


def deposito(saldo, extrato, /):
    valor_deposito = float(input(f''' Informe o valor do deposito.\n '''))
    if valor_deposito > 0:
        saldo_retorno = saldo + valor_deposito
        print(f''' Deposito efetuado, R${valor_deposito:.2f} foi creditado em sua conta.\n''')
        return saldo_retorno, extrato + f'''
    Deposito efetuado.......R${valor_deposito:.2f}\n'''
    else:
        print(f''' Valor inválido!!''')
        return saldo, extrato


def saque(*, saldo, extrato, limite, quantidade_saque, limite_saque):
    if quantidade_saque < limite_saque:
        valor_saque = float(input(f''' Informe o valor de saque.\n '''))
        if 0 < valor_saque <= limite and valor_saque <= saldo:
            saldo -= valor_saque
            print(f''' Saque realizado no valor de R${valor_saque:.2f}.\n ''')
            return saldo, extrato + f'''
    Saque efetuado............R${valor_saque:.2f}\n''', quantidade_saque + 1
        elif valor_saque > limite:
            print(f''' O valor máximo de saque é de R${limite}.\n ''')
            return saldo, extrato, quantidade_saque
        elif valor_saque <= 0:
            print(f''' Valor inválido! \n ''')
            return saldo, extrato, quantidade_saque
        elif valor_saque > saldo:
            print(f''' Saldo insuficiente! \n ''')
            return saldo, extrato, quantidade_saque
    else:
        print(f''' Você atingiu o limite de saque. \n ''')
        return saldo, extrato, quantidade_saque


def gerar_extrato(saldo, /, *, extrato):
    print(f'''    Extrato Bancario
    {extrato}    
    Saldo atual = R${saldo}\n''')


def criar_usuario(lista_usuarios):
    cpf = int(input(f''' Digite seu cpf somente números.\n '''))
    verificado_cpf = verificar_cpf(cpf, lista_usuarios)
    if verificado_cpf:
        print(f''' Usuario já existe''')
        return lista_usuarios
    elif verificado_cpf is None:
        nome = input(f''' Digite seu nome completo.\n ''')
        data_nascimento = input(f''' Digite sua data de nascimento (dd-mm-aaaa).\n ''')
        endereco = input(f''' Digite endereço no formato (logradouro, número - bairro - cidade/sigla do estado).\n ''')
        return lista_usuarios + [{'cpf': cpf, 'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco}]


def criar_conta(lista_contas, agencia, lista_usuarios, quantidade_contas):
    cpf = int(input(f''' Digite seu cpf somente números.\n '''))
    verificado_cpf = verificar_cpf(cpf, lista_usuarios)
    if verificado_cpf is None:
        print(f''' Você deve criar um usuário primeiro.\n ''')
        return lista_contas, quantidade_contas
    elif verificado_cpf:
        quantidade_contas += 1
        print(f''' Conta criada com sucesso
        ag: {agencia}
        c.c: {quantidade_contas}''')
        return lista_contas +[{'cpf': cpf, 'agencia': agencia, 'conta': quantidade_contas}], quantidade_contas


def verificar_cpf(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario['cpf'] == cpf:
            return True
    else:
        return None


def main():
    LIMITE_SAQUE = 3
    AGENCIA = '0001'

    quantidade_saque = 0
    quantidade_contas = 0
    saldo = 0
    limite = 500
    extrato = ''
    lista_usuarios = []
    lista_contas = []

    while True:
        open_menu = menu()

        if open_menu == 0:
            break

        elif open_menu == 1:
            saldo, extrato = deposito(saldo, extrato)

        elif open_menu == 2:
            saldo, extrato, quantidade_saque = saque(saldo=saldo, extrato=extrato, limite=limite, quantidade_saque=quantidade_saque, limite_saque=LIMITE_SAQUE)

        elif open_menu == 3:
            gerar_extrato(saldo, extrato=extrato)

        elif open_menu == 4:
            lista_usuarios = criar_usuario(lista_usuarios)

        elif open_menu == 5:
            lista_contas, quantidade_contas = criar_conta(lista_contas, AGENCIA, lista_usuarios, quantidade_contas)

        elif open_menu == 6:
            print(f'''Lista de contas abertas.\n ''')
            for conta in lista_contas:
                print(f'''    Ag: {conta['agencia']}
                C.c: {conta['conta']}
                cpf: {conta['cpf']} 
                ''')

main()
