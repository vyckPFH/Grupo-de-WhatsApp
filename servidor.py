import socket
import threading
from time import sleep

HOST = "0.0.0.0"
PORT = 9002

FILA = []
# Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos

WAITING_TIME = 3

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

def inclui_na_fila(mensagem):
     print("adicionando mensagem a fila...")
     produzir(mensagem)
     
def atender_cliente(conn, addr):
    print(f"[Server] Nova conexão {addr}", flush=True)

    with conn:
        nome = conn.recv(1024)
        
        nickname = nome.decode("utf-8")
        print(f"[Server] Recebido de {addr}: {nickname}", flush=True )
        
        conn.sendall("conectado com sucesso! você é: {nickname}".encode("utf-8"))

        print(f"[Server] Respondido para {addr}: {nickname}", flush=True)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            inclui_na_fila(data)
            conn.sendall("OK!".encode("utf-8"))
            print(data.decode("utf-8"))

    print(f"[Server] Conexão encerrada {addr}", flush=True)


def iniciar_servidor():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()

            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, addr),
                daemon=True
            )
            thread.start()


if __name__ == "__main__":
    iniciar_servidor()