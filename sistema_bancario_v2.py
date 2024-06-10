from abc import ABC, abstractmethod
from datetime import date, datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._saldo = 0
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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
        if valor > self._saldo:
            print("Operação não realizada! Você não tem saldo suficiente. Por favor, consulte seu saldo.")
        elif valor > 0:
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor))
            print(f"Saque realizado com sucesso! Você sacou R$ {valor:.2f}.")            
            return True
        else:
            print("Operação não realizada! Valor de saque inválido.")
        return False
            
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print(f"Depósito realizado com sucesso! Você depositou R$ {valor:.2f}.")
            return True
        else:
            print("Operação não realizada! Valor de depósito inválido.")
        return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.depositos_hoje = 0
        self.ultima_data_deposito = None

    def depositar(self, valor):
        hoje = datetime.today().date()

        if self.ultima_data_deposito != hoje:
            self.depositos_hoje = 0
            self.ultima_data_deposito = hoje

        if self.depositos_hoje + valor > self.limite:
            print(f"Operação não realizada! Limite diário de depósito de R$ {self.limite:.2f} excedido.")
            return False

        self.depositos_hoje += valor
        return super().depositar(valor)
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_limite_saques = numero_saques >= self.limite_saques
        if excedeu_limite:
            print(f"Operação não realizada! Limite de saque excedido. O limite é de R$ {self.limite:.2f}.")
        elif excedeu_limite_saques:
            print("Operação não realizada! Você excedeu o número de saques diários.")        
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia} 
            C/C:\t\t{self.numero} 
            Titular:\t{self.cliente.nome}
            CPF:\t\t{self.cliente.cpf} 
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
                "data": datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def menu():
     """

============Olá, Bem-Vindo!============

        1 - Depositar
        2 - Sacar
        3 - Consultar Saldo
        4 - Extrato
        5 - Novo cliente
        6 - Listar clientes
        7 - Criar conta
        8 - Listar contas de um cliente
        0 - Sair
========================================
"""

def validar_valor(mensagem):
    while True:
        valor = input(mensagem)
        try:
            valor = float(valor.replace(",", "."))
            if valor < 0:
                print("\nNão é possível depositar ou sacar um valor negativo.")
                continue
            return valor
        except ValueError:
            print("\nValor inválido. Por favor, insira um número válido.")

def depositar(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)
    if cliente:
        conta = listar_conta_clientes(cliente)
        if conta:
            valor = validar_valor("Informe o valor a ser depositado: R$ ")
            if conta.depositar(valor):
                return True
    else:
        print("\nCPF não encontrado. Por favor, tente novamente.")
        return False

def sacar(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)
    if cliente:
        conta = listar_conta_clientes(cliente)
        if conta:
            valor = validar_valor("Informe o valor a ser sacado: R$ ")
            if valor is not None:
                if conta.sacar(valor):
                    return True
                
    else:
        print("\nCPF não encontrado. Por favor, tente novamente.")
        return False

def imprimir_extrato(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("\nCPF não encontrado. Por favor, tente novamente.")
        return

    conta = listar_conta_clientes(cliente)
    if not conta:
        return

    print("\n============== EXTRATO ================")
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Não há transações para exibir.")
        return
    
    transacoes.sort(key=lambda x: x['data'])

    saldo_atual = 0

    extrato_depositos = []
    extrato_saques = []

    for transacao in transacoes:
        tipo = transacao['tipo']
        valor = transacao['valor']
        data = transacao['data']
        linha = f"Data Mov: {data} | Tipo: {tipo} | Titular: {conta.cliente.nome} | Valor: R$ {valor:.2f}"

        if tipo == 'Deposito':
            saldo_atual += valor
            extrato_depositos.append(linha)
        elif tipo == 'Saque':
            saldo_atual -= valor
            extrato_saques.append(linha)

    print("\n--- Depósitos ---")
    for linha in extrato_depositos:
        print(linha)
    
    print("\n--- Saques ---")
    if not extrato_saques:
        print("Você não realizou nenhum saque.")
    else:
        for linha in extrato_saques:
            print(linha)

    print(f"\nSaldo Atual:\n\tR$ {saldo_atual:.2f}")
    print("============== FIM DO EXTRATO ================")

def criar_usuario(clientes):
    while True:
        cpf = input("Informe o CPF (somente números): ")
        cliente = filtrar_usuarios(cpf, clientes)
    
        if cliente:
            print("\nCPF já cadastrado. Por favor, tente novamente.")
            return
        nome = input("Informe o nome do cliente: ")
        while True:
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            try:
                datetime.strptime(data_nascimento, '%d/%m/%Y')
                break
            except ValueError:
                print("Formato de data inválido. Por favor, digite no formato dd/mm/aaaa.")
        
        endereco = input("Informe o endereço completo (logradouro, número - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf,
                       endereco=endereco)
        clientes.append(cliente)
        print("Cliente criado com sucesso!")
        
        cadastrar_outro_usuario = input("Deseja cadastrar outro cliente? (S/N): ").upper()  
        if cadastrar_outro_usuario != 'S':
            break
        
def filtrar_usuarios(cpf, clientes):
    lista_clientes = [cliente for cliente in clientes if cliente.cpf == cpf]
    return lista_clientes[0] if lista_clientes else None

def criar_conta(numero_conta, clientes, contas):
    while True:
        cpf = input("Informe o CPF (somente números): ")
        cliente = filtrar_usuarios(cpf, clientes)
        if not cliente:
            print("CPF não encontrado. Tente novamente.")
        else:
            conta = ContaCorrente(cliente=cliente,
            numero=numero_conta)
            contas.append(conta)
            cliente.contas.append(conta)
            print("Conta criada com sucesso!")
            numero_conta += 1  

        cadastrar_outra_conta = input("Deseja cadastrar outra conta? (S/N): ").upper()  
        if cadastrar_outra_conta != 'S':
            break

def listar_conta_clientes(cliente):
    if not cliente.contas:
        print("O cliente não possui contas cadastradas.")
        return
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    # se a conta não existe , informa uma mensagem , caso exista informa o procedimento acima
    if not contas:
        print("Não há contas cadastradas.")
        return
    # FIXME: não permite escolher a conta
    return contas[0]
        
menu = """

============Olá, Bem-Vindo!============

        1 - Depositar
        2 - Sacar
        3 - Extrato
        4 - Novo cliente
        5 - Criar conta
        6 - Listar contas de um cliente 
        0 - Sair
========================================
"""
def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu + "Informe a opção desejada: ")

        try:
            opcao = int(opcao)
            if opcao == 0:
                print("\nObrigado por usar o sistema bancário! Até logo.\n")
                break
            elif opcao == 1:
                depositar(clientes)
            elif opcao == 2:
                sacar(clientes)
            elif opcao == 3:
                imprimir_extrato(clientes)
            elif opcao == 4:
                criar_usuario(clientes)
            elif opcao == 5:
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            elif opcao == 6:
                listar_contas(contas)
            else:
                print("\nOpção inválida. Tente novamente.\n")
        except ValueError:
            print("\nOpção inválida. Por favor, insira um número.\n")

main()
