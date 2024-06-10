# Sistema_bancario_v2
Modelando sistema bancario com POO

Este é um sistema bancário simples implementado em Python. Ele permite a criação de clientes e contas bancárias, além de realizar operações básicas como depósitos, saques e consulta de extratos.

## Funcionalidades

- **Criar Clientes:** Registre novos clientes no sistema.
- **Criar Contas Correntes:** Crie contas correntes associadas a clientes.
- **Depósitos:** Realize depósitos em contas correntes.
- **Saques:** Realize saques respeitando limites de saldo e quantidade de saques diários.
- **Consultar Extrato:** Exiba o extrato das transações realizadas.
- **Listar Contas:** Liste todas as contas registradas no sistema.

## Classes e Estrutura

### Cliente
Classe base para clientes, armazena informações básicas e a lista de contas associadas.

### PessoaFisica
Subclasse de `Cliente`, adiciona informações específicas para pessoas físicas como nome, CPF e data de nascimento.

### Conta
Classe que representa uma conta bancária genérica, com métodos para sacar e depositar dinheiro.

### ContaCorrente
Subclasse de `Conta`, adiciona funcionalidades específicas para contas correntes, como limites de saque e depósito diário.

### Historico
Classe que armazena o histórico de transações realizadas em uma conta.

### Transacao
Classe abstrata que serve de base para transações bancárias.

### Saque e Deposito
Subclasses de `Transacao` que implementam as operações de saque e depósito.

## Como Usar

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/sistema-bancario-python.git
   cd sistema-bancario-python


2. Execute o script `main.py`:
    ```sh
   python main.py


3. Siga as instruções no menu para realizar as operações desejadas.

## Estrutura do Menu

O menu principal oferece as seguintes opções:

```
============Olá, Bem-Vindo!============

        1 - Depositar
        2 - Sacar
        3 - Extrato
        4 - Novo cliente
        5 - Criar conta
        6 - Listar contas de um cliente 
        0 - Sair
========================================
```

### Exemplo de Uso

#### Criar um Novo Cliente
Selecione a opção `4` e siga as instruções para fornecer os detalhes do cliente.

#### Criar uma Nova Conta
Selecione a opção `5` após criar um cliente e forneça os detalhes da conta.

#### Realizar um Depósito
Selecione a opção `1`, insira o CPF do cliente e o valor a ser depositado.

#### Realizar um Saque
Selecione a opção `2`, insira o CPF do cliente e o valor a ser sacado.

#### Consultar o Extrato
Selecione a opção `3`, insira o CPF do cliente para visualizar o extrato das transações.

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, encontre um bug ou quiser adicionar novas funcionalidades, por favor, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
