import socket

# HOST = "192.168.247.135"
HOST = "192.168.18.79"

PORT = 9002

nickname = input("Nickname: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    # envia nickname
    cliente.sendall(nickname.encode("utf-8"))

    # espera confirmação de conexão
    resposta = cliente.recv(1024).decode("utf-8")
    print(f"[Server] {resposta}")

    while True:
        msg = input("Mensagem: ")

        if not msg:
            continue

        cliente.sendall(msg.encode("utf-8"))

        # espera confirmação do servidor
        resposta = cliente.recv(1024).decode("utf-8")

        if resposta != "OK":
            print("[ERRO] servidor não confirmou recebimento")
        else:
            print("enviado com sucesso")