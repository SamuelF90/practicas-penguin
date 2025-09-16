import socket

def cliente_simple():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))

    try:
        while True:
            mensaje = input("Escribe mensaje para enviar (o 'salir' para terminar): ")
            if mensaje.lower() == 'salir':
                break
            sock.sendall(mensaje.encode())

            data = sock.recv(1024)
            print(f"Recibido del servidor: {data.decode()}")
    finally:
        sock.close()

if __name__ == "__main__":
    cliente_simple()
