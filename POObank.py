
from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
import datetime
import pytz

# Classe CONTA
class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0.0
    self._numero = numero
    self._agencia = '0001'
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

  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)

  def sacar(self, valor):
    if valor > self._saldo:
      print('Você não possui saldo suficiente para realizar esse saque.')
      return False

    elif valor > 0:
      print(f'Você sacou R$ {valor}')
      self._saldo = self._saldo - valor
      return True

    else:
      print('Valor inválido.')
      return False

  def depositar(self, valor):
    if valor > 0:
      print(f'Você depositou R$ {valor}')
      return True

    else:
      print('Valor inválido.')
      return False

# Classe CONTACORRENTE
class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite = 500.0, limite_saques = 3):
    super().__init__(numero, cliente)
    self._limite = limite
    self._limite_saques = limite_saques

  @property
  def limite(self):
    return self._limite

  @property
  def limite_saques(self):
    return self._limite_saques

  def sacar(self, valor):
    numero_saques = 0

    for transacao in self._historico.transacoes:
      if transacao['tipo'] == Saque:
        numero_saques = numero_saques + 1

    if numero_saques == self._limite_saques:
      print('O limite de saques diários já foi atingido.')
      return False

    elif valor > self._limite:
      print('O valor desejado é maior do que seu valor limite por saque.')
      return False

    elif valor > self._saldo:
      print('Você não possui saldo suficiente para realizar esse saque.')
      return False

    elif valor > 0:
      print(f'Você sacou R$ {valor}')
      self._saldo = self._saldo - valor
      return True

    else:
      print('Valor inválido.')
      return False

# Classe CLIENTE
class Cliente:
  def __init__(self, endereco):
    self._endereco = endereco
    self._contas = []

  @property
  def endereco(self):
    return self._endereco

  @property
  def contas(self):
    return self._contas

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)
  
  def adicionar_conta(self, conta):
    self._contas.append(conta)

# Classe PESSOAFISICA
class PessoaFisica(Cliente):
  def __init__(self, endereco, cpf, nome, data_nascimento):
    super().__init__(endereco)
    self._cpf = cpf
    self._nome = nome
    self._data_nascimento = data_nascimento

  @property
  def cpf(self):
    return self._cpf

  @property
  def nome(self):
    return self._nome

  @property
  def data_nascimento(self):
    return self._data_nascimento

# Classe HISTORICO
class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

  def adicionar_transacao(self, transacao):
    self._transacoes.append(
        {
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data_hora': transacao.horario
        }
    )

# Classe TRANSACAO
class Transacao(ABC):

  @abstractclassmethod
  def registrar(self):
    pass

# Classe DEPOSITO
class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    if conta.depositar(self._valor):
      conta.historico.adicionar_transacao(self)

# Classe SAQUE
class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    if conta.sacar(self._valor):
      conta.historico.adicionar_transacao(self)
