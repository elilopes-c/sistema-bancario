import textwrap
from abc import ABC
from datetime import datetime


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

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
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    @property
    def limite(self): 
        return self._limite

    @property
    def limite_saques(self): 
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao_info): 
        self._transacoes.append(transacao_info)

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        contador_transacoes_do_dia = 0
        data_atual = datetime.now().date()
        for transacao in self.gerar_relatorio():
            # Verifica se 'data' existe na transação antes de tentar converter
            if "data" in transacao:
                data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
                if data_transacao == data_atual:
                    contador_transacoes_do_dia += 1
        return contador_transacoes_do_dia


class Transacao(ABC):
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]


@log_transacao
# Função DEPOSITAR: Argumentos APENAS POR POSIÇÃO
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append({
            "tipo": "Deposito",
            "valor": valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        print("\n=== Depósito realizado com sucesso! ===")
        return saldo, extrato
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato


@log_transacao
# Função SACAR: Argumentos APENAS POR NOME
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): 
    limite_transacoes_diarias = 10 # Limite de transações diárias

    # Validação de limite diário de transações para saque
    transacoes_do_dia = 0
    data_atual = datetime.now().date()
    for t in extrato: # Usamos a lista de extrato passada como argumento
        if "data" in t:
            data_transacao = datetime.strptime(t["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_transacao == data_atual and t["tipo"] == "Saque": # Apenas saques contam para este limite
                transacoes_do_dia += 1
    
    if transacoes_do_dia >= limite_transacoes_diarias:
        print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
        return saldo, extrato # Retorna saldo e extrato sem alteração

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato.append({
            "tipo": "Saque",
            "valor": valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        print("\n=== Saque realizado com sucesso! ===")
        return saldo, extrato
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato # Retorna saldo e extrato sem alteração se a operação falhar


@log_transacao
# Função EXIBIR_EXTRATO: Argumento POSICIONAL e NOMEADO
def exibir_extrato(saldo, /, *, extrato): 
    print("\n================ EXTRATO ================")
    extrato_str = ""
    tem_transacao = False
    for transacao in extrato: # Itera sobre a lista de extrato passada como argumento
        tem_transacao = True
        extrato_str += f"\n{transacao['tipo']}:"
        extrato_str += f"\n\tData: {transacao['data']}"
        extrato_str += f"\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato_str = "Não foram realizadas movimentações"

    print(extrato_str)
    print(f"\nSaldo:\n\tR$ {saldo:.2f}") # Usa o saldo passado como argumento posicional
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    # Limpa o CPF de caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf)) 
    
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500, limite_saques=3) 
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas): 
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main(): 
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            valor = float(input("Informe o valor do depósito: "))
            
            # Chama a função depositar com argumentos posicionais
            conta._saldo, conta._historico._transacoes = depositar(
                conta.saldo,
                valor,
                conta.historico.transacoes,
            )

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue
            
            valor = float(input("Informe o valor do saque: "))

            # Chama a função sacar com argumentos nomeados
            numero_saques = len(
                [t for t in conta.historico.transacoes if t["tipo"] == "Saque"]
            )
            
            conta._saldo, conta._historico._transacoes = sacar(
                saldo=conta.saldo,
                valor=valor,
                extrato=conta.historico.transacoes,
                limite=conta.limite, # Acesso ao limite da conta corrente
                numero_saques=numero_saques,
                limite_saques=conta.limite_saques # Acesso ao limite de saques da conta corrente
            )

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue
            
            # Chama a função exibir_extrato com argumento posicional e nomeado
            exibir_extrato(conta.saldo, extrato=conta.historico.transacoes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()