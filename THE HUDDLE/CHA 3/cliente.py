import socket
import threading
import time

def conectar_servidor():
    for intento in range(5):
        try:
            s = socket.socket()
            s.connect(('localhost', 8000))
            return s
        except ConnectionRefusedError:
            print("Reintentando conexión...")
            time.sleep(2)
    print("No se pudo conectar al servidor.")
    return None

def recibir_mensajes(s):
    while True:
        try:
            mensaje = s.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(mensaje)
        except:
            break

def main():
    s = conectar_servidor()
    if not s:
        return

    hilo = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
    hilo.start()

    while True:
        try:
            mensaje = input()
            if mensaje.lower() == 'salir':
                break
            s.send(mensaje.encode('utf-8'))
        except:
            break

    s.close()

if __name__ == "__main__":
    main()


