#SERVIDOR 2 

import selectors
import socket

#CREAR SELECTOR
selectors = selectors.DefaultSelector()

#FUNCION PARA CREAR NUEVAS CONEXIONES
def accept(sock, mask):
    conn, addr = sock.accept()
    print(f"Cliente conectado desde {addr}")
    conn.setblocking(False)
    selectors.register(conn, selectors.EVENT_READ , read)

# Función para leer datos de un cliente
def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print(f"Recibido: {data.decode()}")
        conn.sendall(data)  # Eco
    else:
        print("Cliente desconectado")
        selectors.unregister(conn)
        conn.close()

# Crear socket servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5000))
sock.listen()
sock.setblocking(False)

# Registrar el socket principal para aceptar conexiones
sel.register(sock, selectors.EVENT_READ, accept)

print("Servidor escuchando en puerto 5000...")

# Bucle principal
while True:
    events = sel.select()  # Espera eventos
    for key, mask in events:
        callback = key.data  # La función asociada (accept o read)
        callback(key.fileobj, mask)