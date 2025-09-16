import socket
import selectors

sel = selectors.DefaultSelector()
clientes = {}
aliases = set()

def aceptar_conexion(sock):
    conexion, addr = sock.accept()
    conexion.setblocking(False)
    sel.register(conexion, selectors.EVENT_READ, manejar_mensaje)
    print(f"[+] Cliente conectado desde {addr}")
    conexion.send("Escribe tu alias: ".encode('utf-8'))

def manejar_mensaje(conexion):
    try:
        mensaje = conexion.recv(1024)
        if not mensaje:
            desconectar_cliente(conexion)
            return

        mensaje = mensaje.decode('utf-8').strip()

        if conexion not in clientes:
            if mensaje in aliases:
                conexion.send("Alias en uso. Usa otro: ".encode('utf-8'))
                return
            clientes[conexion] = mensaje
            aliases.add(mensaje)
            print(f"[+] Alias asignado: {mensaje}")
            broadcast(f"{mensaje} se ha unido al chat.", conexion)
        else:
            if mensaje.startswith("/"):
                procesar_comando(conexion, mensaje)
            else:
                alias = clientes[conexion]
                broadcast(f"{alias}: {mensaje}", conexion)

    except ConnectionResetError:
        desconectar_cliente(conexion)

def procesar_comando(conexion, mensaje):
    if mensaje == "/ayuda":
        ayuda = "Comandos disponibles:\n/lista - Ver usuarios conectados\n/ayuda - Mostrar esta ayuda"
        conexion.send(ayuda.encode('utf-8'))
    elif mensaje == "/lista":
        lista = "Usuarios conectados:\n" + "\n".join(aliases)
        conexion.send(lista.encode('utf-8'))
    else:
        conexion.send("Comando no reconocido. Escribe /ayuda para ver opciones.".encode('utf-8'))

def broadcast(mensaje, emisor):
    for cliente in clientes:
        if cliente != emisor:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                desconectar_cliente(cliente)

def desconectar_cliente(conexion):
    alias = clientes.get(conexion, "Desconocido")
    print(f"[-] Cliente desconectado: {alias}")
    if conexion in clientes:
        aliases.discard(clientes[conexion])
        del clientes[conexion]
    sel.unregister(conexion)
    conexion.close()
    broadcast(f"{alias} se ha desconectado.", conexion)

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 8000))
    servidor.listen()
    servidor.setblocking(False)
    sel.register(servidor, selectors.EVENT_READ, aceptar_conexion)

    print("Servidor escuchando en el puerto 8000...")

    try:
        while True:
            eventos = sel.select()
            for key, _ in eventos:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        print("\nServidor cerrado.")
    finally:
        sel.close()
        servidor.close()

if __name__ == "__main__":
    main()

