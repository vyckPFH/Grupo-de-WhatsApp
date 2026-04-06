import socket

HOST = "127.0.0.1"
PORT = 9040


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    # conn = cliente.accept()
    while True:
        resposta = cliente.recv(1024).decode("utf-8")
        print(f"[Server] {resposta}")