import socket

# HOST = "192.168.247.135"
# HOST = "192.168.18.79"
HOST = ""
PORT = 9003

HOST = input("Digite o IP do servidor: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    print("Conectado ao servidor de mensagens")

    while True:
        try:
            data = cliente.recv(1024)

            if not data:
                print("Servidor desconectou")
                break

            print(f"[Server] {data.decode('utf-8')}")

        except Exception as e:
            print(f"Erro: {e}")
            break