import threading
from time import sleep
import socket
import threading

# Fila de mensagens
FILA = []

# Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos

HOST = "0.0.0.0"
PORT = 9050

def atender_cliente_env(conn, addr):
    print(f"[Server] Nova conexão {addr}", flush=True)

    with conn:
        nomeCliente = conn.recv(1024)

        nome = nomeCliente.decode("utf-8")

        data = conn.recv(1024)
        mensagem = data.decode("utf-8")
        print(f"[Server] Recebido de {addr}: {nome}: {mensagem}", flush=True )
        # ip do remetente, nome do remetente, msg e horario da msg é aq q bota
        # sleep(WAITING_TIME)
        
        conn.sendall(mensagem.encode("utf-8"))

        print(f"[Server] Respondido para {addr}: {mensagem}", flush=True)


    print(f"[Server] Conexão encerrada {addr}", flush=True)


def atender_cliente_recv(conn, addr):
    print(f"[Server] Nova conexão {addr}", flush=True)

    with conn:
        data = conn.recv(1024)

        mensagem = data.decode("utf-8")
        print(f"[Server] Recebido de {addr}: {mensagem}", flush=True )

        print(f"[Server] Processando mensagem..", flush=True )
        resposta = mensagem.upper()
        # sleep(WAITING_TIME)
        
        conn.sendall(resposta.encode("utf-8"))

        print(f"[Server] Respondido para {addr}: {resposta}", flush=True)


    print(f"[Server] Conexão encerrada {addr}", flush=True)


def iniciar_servidorPortaClienteENV():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()

            thread = threading.Thread(
                target=atender_cliente_env,
                args=(conn, addr),
                daemon=True
            )
            thread.start()


def produzir(mensagem):
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Inclui a mensagem na fila
    FILA.append(mensagem)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Informa que há itens na fila.
    SEMAFORO_ITENS.release() 

def consumir():
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda até que existam itens na fila
    SEMAFORO_ITENS.acquire()

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Verifica se há mensagens na fila
    if FILA:
        # Retira a primeira mensagem da fila
        mensagem = FILA.pop(0)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Retorna a mensagem que estava na fila
    return mensagem

def thread_produtora(id_thread):
    # Inclui mensagens na fila
    id_msg = 0
    
    while True:
        msg_produzida = f"Mensagem {id_msg}"
        print(f"[Thread {id_thread} produziu] {msg_produzida}", flush=True)
        produzir(msg_produzida)
        id_msg += 1
        sleep(1)

def thread_consumidora(id_thread):
    # Retira mensagens da fila
    while True:
        msg_consumida = consumir()
        print(f"[Thread {id_thread} consumiu] {msg_consumida}", flush=True)
        sleep(1)

def criarThreads():
     # Cria a thread produtora
    t0 = threading.Thread(
                target=thread_produtora, args=(0,), # Será a thread 0
                daemon=True
            )

    # Cria 2 threads consumidoras
    t1 = threading.Thread(
                target=thread_consumidora, args=(1,), # Será a thread 1
                daemon=True
            )
    t2 = threading.Thread(
                target=thread_consumidora, args=(2,), # Será a thread 2
                daemon=True
            )
    
    t0.start()
    t1.start()
    t2.start()

    t0.join()
    t1.join()
    t2.join()

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    #     serv.bind((HOST, PORT))
    #     serv.listen()
        
    #     addr, conn  = serv.accept()    
    #     print("{addr} conectou")    
    #     atender_cliente_env(addr, conn)

if __name__ == "__main__":
    main()
