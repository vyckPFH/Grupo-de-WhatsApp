import socket

HOST = "192.168.245.106"
PORT = 9050

name = input("[Cliente] Nome de usuario: ")
mensagem = input("[Cliente] Mensagem: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    cliente.sendall(mensagem.encode("utf-8"))

    resposta = cliente.recv(1024).decode("utf-8")

    print(f"[Server] {resposta}")