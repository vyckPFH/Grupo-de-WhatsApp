import socket

HOST = "192.168.247.135"
PORT = 9003


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    # conn = cliente.accept()
    while True:
        resposta = cliente.recv(1024).decode("utf-8")
        print(f"[Server] {resposta}")