# Chat com Fila de Mensagens — Instruções de Execução

Sistema de chat multiusuário utilizando **sockets TCP**, **threads** e **semáforos** em Python.

---

## Arquivos do projeto

| Arquivo | Descrição |
|---|---|
| `servidor.py` | Gerencia conexões e a fila de mensagens |
| `cliente_env.py` | Envia mensagens ao servidor |
| `cliente_recv.py` | Recebe e exibe mensagens de todos os clientes |

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária (apenas módulos padrão)
- As maquinhas devem estar todas na mesma rede para que este código funcione

---

## Como executar

### 1. Iniciar o servidor

No terminal da máquina que será o servidor, execute:

```bash
python servidor.py
```

O servidor ficará ouvindo nas portas:
- **9002** — para clientes que enviam mensagens
- **9003** — para clientes que recebem mensagens

---

### 2. Iniciar o cliente receptor (`cliente_recv.py`)

> Recomenda-se iniciar este cliente **antes** de enviar mensagens, para não perdê-las.

Em um terminal (pode ser na mesma máquina ou em outra na rede):

```bash
python cliente_recv.py
```

Informe o IP do servidor quando solicitado. Exemplo:

```
IP do servidor: 192.168.1.10
```

---

### 3. Iniciar o cliente emissor (`cliente_env.py`)

Em outro terminal:

```bash
python cliente_env.py
```

Informe o IP do servidor e seu nome:

```
IP do servidor: 192.168.1.10
Digite seu nome: Celso
```

Após a confirmação de conexão, basta digitar as mensagens e pressionar **ENTER** para enviar.

---

## Exemplo de mensagem exibida

```
[Celso (192.168.10.40) 17:21:15]
Oi pessoal.
```

---

## Observações

- Múltiplos clientes podem se conectar simultaneamente em ambas as portas.
- O acesso à fila de mensagens é protegido por semáforos, evitando condições de corrida.
- Para encerrar qualquer cliente, pressione **Ctrl+C**.
- O servidor pode ser executado localmente (`127.0.0.1`) para testes na mesma máquina.
