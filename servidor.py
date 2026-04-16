import socket              # biblioteca para comunicação em rede (TCP)
import threading           # permite usar threads (execução paralela)
from time import sleep     # função para pausar execução

# IP do servidor (0.0.0.0 = aceita conexão de qualquer lugar)
HOST = "0.0.0.0"

# Portas usadas
PORTA_ENV = 9002   # clientes que ENVIAM mensagens
PORTA_RECV = 9003  # clientes que RECEBEM mensagens

# ---------------- FILA ----------------

FILA = []  # lista compartilhada onde ficam as mensagens

# Semáforo: controla acesso à fila (1 thread por vez)
SEMAFORO_ACESSO = threading.Semaphore(1)

# Semáforo: conta quantos itens existem na fila
SEMAFORO_ITENS = threading.Semaphore(0)

# ---------------- CLIENTES RECV ----------------

CLIENTES_RECV = []  # lista com conexões dos clientes que recebem mensagens

# Semáforo: protege a lista de clientes
SEMAFORO_CLIENTES = threading.Semaphore(1)


# ---------------- PRODUZIR ----------------
def produzir(mensagem):
    # trava acesso à fila
    SEMAFORO_ACESSO.acquire()

    # adiciona mensagem na fila
    FILA.append(mensagem)

    # libera acesso à fila
    SEMAFORO_ACESSO.release()

    # avisa que existe um novo item na fila
    SEMAFORO_ITENS.release()


# ---------------- CONSUMIR ----------------
def consumir():
    # espera até existir pelo menos 1 item
    SEMAFORO_ITENS.acquire()

    # trava acesso à fila
    SEMAFORO_ACESSO.acquire()

    # remove o primeiro item da fila
    mensagem = FILA.pop(0)

    # libera acesso à fila
    SEMAFORO_ACESSO.release()

    # retorna a mensagem retirada
    return mensagem


# ---------------- CLIENTE ENV (ENVIA DADOS) ----------------
def atender_cliente_env(conn, addr):
    print(f"[ENV] Nova conexão {addr}")

    # "with conn" garante que a conexão será fechada automaticamente no final
    with conn:

        # recebe o nome do cliente
        nome = conn.recv(1024)

        # converte bytes para string
        nickname = nome.decode("utf-8")

        print(f"[ENV] {addr} nome: {nickname}")

        # envia confirmação para o cliente
        conn.sendall(f"Conectado como {nickname}".encode())

        # loop para receber mensagens continuamente
        while True:
            data = conn.recv(1024)

            # se não veio nada → cliente desconectou
            if not data:
                break

            # monta mensagem com nome do usuário
            mensagem = f"{nickname}: {data.decode()}".encode()

            # coloca mensagem na fila
            produzir(mensagem)

            # responde ao cliente
            conn.sendall(b"OK")

    print(f"[ENV] Conexão encerrada {addr}")


# ---------------- CLIENTE RECV (RECEBE DADOS) ----------------
def atender_cliente_recv(conn, addr):
    print(f"[RECV] Cliente conectado {addr}")

    SEMAFORO_CLIENTES.acquire() # pega a fila de clientes só pra ela
    try:
        CLIENTES_RECV.append(conn) #tenta adicionar a conexao a lista de conexoes, como se adicionase no "grupo"
    finally:
        SEMAFORO_CLIENTES.release() #libera a fila de clientes

    try:
        while True:
            data = conn.recv(1024)

            # se cliente desconectou
            if not data:
                break

    finally:
        SEMAFORO_CLIENTES.acquire() #pega os clientes e remove aquele que desconectou.
        try:
            CLIENTES_RECV.remove(conn)
        finally:
            SEMAFORO_CLIENTES.release()

        conn.close()
        print(f"[RECV] Cliente desconectado {addr}")


# ---------------- CONSUMIDOR (ENVIA PARA TODOS) ----------------
def thread_consumidora():
    while True:
        # pega mensagem da fila
        msg = consumir()

        # trava acesso à lista de clientes
        SEMAFORO_CLIENTES.acquire()
        for cliente in CLIENTES_RECV:
            try:
                cliente.sendall(msg)
            except Exception:
                # remove cliente com segurança
                try:
                    if cliente in CLIENTES_RECV:
                        CLIENTES_RECV.remove(cliente)
                # fecha conexão
                finally:
                    try:
                        cliente.close()
                    except:
                        print("algo deu errado na linha 153")
    
        SEMAFORO_CLIENTES.release()


# ---------------- SERVIDOR ENV ----------------
def abrir_conexao_cliente_env(porta):

    # cria socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # permite reutilizar porta rapidamente
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # associa socket ao IP e porta
        s.bind((HOST, porta))

        # coloca servidor em modo de escuta
        s.listen()

        print(f"[ENV] ouvindo em {porta}")

        while True:
            # aceita nova conexão
            conn, addr = s.accept()

            # cria thread para atender cliente
            threading.Thread(
                target=atender_cliente_env,
                args=(conn, addr),
                daemon=True
            ).start()


# ---------------- SERVIDOR RECV ----------------
def abrir_coneccao_cliente_RECV(porta):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, porta))
        s.listen()

        print(f"[RECV] ouvindo em {porta}")

        while True:
            conn, addr = s.accept()

            threading.Thread(
                target=atender_cliente_recv,
                args=(conn, addr),
                daemon=True
            ).start()


# ---------------- INICIAR SERVIDOR ----------------
def iniciar_servidor():

    # thread que recebe mensagens (ENV)
    t1 = threading.Thread(target=abrir_conexao_cliente_env, args=(PORTA_ENV,), daemon=True)

    # thread que gerencia clientes que recebem (RECV)
    t2 = threading.Thread(target=abrir_coneccao_cliente_RECV, args=(PORTA_RECV,), daemon=True)

    # thread que consome fila e envia mensagens
    t3 = threading.Thread(target=thread_consumidora, daemon=True)

    # inicia threads
    t1.start()
    t2.start()
    t3.start()

    # mantém programa rodando
    t1.join()
    t2.join()
    t3.join()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    iniciar_servidor()