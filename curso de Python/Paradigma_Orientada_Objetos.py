from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\n Saldo insuficiente')

        elif valor > 0:
            self._saldo -= valor
            print('\n Saque realizado com sucesso!')
            return True

        else:
            print('\n O valor informado é inválido para saque!')

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n Depósito realizado com sucesso!')
        else:
            print('\n O valor informado é inválido para deposito!')
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\n Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente}
            saldo {self.saldo}


        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def verificar_cpf(clientes, cpf):
    
    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]

    if cliente:
        return cliente[0], True
    else:
        return None, None

def menu():
    try:
        opção_menu = int(input(f''' 
          Seja bem vindo!!!
          ############### MENU ###############
          1 - Criar usuario
          2 - Criar conta corrente
          3 - Realizar deposito
          4 - Realizar saque  
          5 - Visalizar extrato
          6 - Listar contas
          0 - Sair do sietma
                               
          O que deseja fazer hoje?\n ~>'''))
    except ValueError:
        print('Opção inválida. Digite uma das opções do menu!')
        return 

    return opção_menu

def criar_usuario(clientes):
    cpf = input(f' Digite cpf somente números.\n ~>')

    cliente, cpf_verificado = verificar_cpf(clientes, cpf)

    if cpf_verificado:
        print(f' \n Usuario já existe!!!')

    elif cpf_verificado is None:
        nome = input(f' Informe seu nome completo.\n ~>')
        data_nasciento = input(f' Informe sua data de nascimento (dd/mm/aaaa).\n ~>')
        endereco = input(f' Informe seu endereço (logradougo, nro - bairro - cidade/sigla estado).\n ~>')

        cliente = PessoaFisica(nome, data_nasciento, cpf, endereco)

        clientes.append(cliente)

        print(f' \n Usuario cadastrado com sucesso!')
    

def criar_conta(contas, clientes):

    cpf = input(f' Digite cpf do usuario, somente números.\n ~>')

    cliente, cpf_verificado = verificar_cpf(clientes, cpf)

    if cpf_verificado:
        numero_conta = len(contas) + 1
        
        nova_conta = ContaCorrente.nova_conta(cpf, numero_conta)

        contas.append(nova_conta)
        cliente.contas.append(nova_conta)
        
        
        print(f' \n Conta criada cm sucesso!')

    elif cpf_verificado is None:
        print(f' \n Usuario não encontrado!')

def realizar_deposito(clientes):
    cpf = input(f' Digite cpf do usuario, somente números.\n ~>')

    cliente, cpf_verificado = verificar_cpf(clientes, cpf)

    if cpf_verificado is None:
        print(f' Usuario não encontrado!')

    elif not cliente.contas:
        print(f' Não há contas para o cpf informado!')

    elif cliente.contas:
        valor = int(input(f' Qual o valor do deposito?\n ~>'))
        operacao = Deposito(valor)

        conta = cliente.contas[0]

        cliente.realizar_transacao(conta, operacao)

        print(conta)

def realizar_sque(clientes):
    cpf = input(f' Digite cpf do usuario, somente números.\n ~>')

    cliente, cpf_verificado = verificar_cpf(clientes, cpf)

    if cpf_verificado is None:
        print(f' \n Usuario nãon encontrado!')

    elif not cliente.contas:
        print(f' \n Não há contas para o cpf informado')
    
    elif cliente.contas:
        valor = int(input(f' Qual o valor do saque? \n ~>'))
        operacao = Saque(valor)

        conta = cliente.contas[0]

        cliente.realizar_transacao(conta, operacao)

        print(conta)

def visualizar_extrato(clientes):
    cpf = input(f' Digite cpf do usuario, somente números.\n ~>')

    cliente, cpf_verificado = verificar_cpf(clientes, cpf)

    conta = cliente.contas[0]

    historico =  conta.historico



    if cpf_verificado is None:
        print(f' Usuario nãon encontrado!')

    elif not cliente.contas:
        print(f'não há contas para o cpf informado')
    
    elif cliente.contas:
        print(f' Extrato Bancario!\n Data:{datetime.now().strftime("%d-%m-%Y")} Hora:{datetime.now().strftime("%H:%M:%S")}\n \n Operação                  valor             data/hora\n')
        
        for transacao in historico.transacoes:
            
            if transacao['tipo'] == 'Deposito':
                str_valor = f'{transacao['valor']:.2f}                                        '
                str_tipo_transacao = f' {transacao['tipo']}                                         '
                print(str_tipo_transacao[:26], str_valor[:17], f'{transacao['data']}')

            if transacao['tipo'] == 'Saque':
                str_valor = f'{transacao['valor']:.2f}                                        '
                str_tipo_transacao = f' {transacao['tipo']}                                         '
                print(str_tipo_transacao[:26], str_valor[:17], f'{transacao['data']}')

        print(f'\n Saldo total R${conta.saldo:.2f}')    
 
def main():
    contas = []
    clientes = []
    
    while True:
        opção_menu = menu()

        if opção_menu == 0:
            break

        elif opção_menu == 1:
            criar_usuario(clientes)

        elif opção_menu == 2:
            criar_conta(contas, clientes)

        elif opção_menu == 3:
            realizar_deposito(clientes)

        elif opção_menu == 4:
            realizar_sque(clientes)

        elif opção_menu == 5:
            visualizar_extrato(clientes)

        elif opção_menu is None:
            pass

        else: 
            print(f' Opção iválida!')

main()