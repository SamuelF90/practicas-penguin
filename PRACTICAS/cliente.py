#CLIENTE SOCKET
import socket
#Crear socket
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Conetarse al servidor
cliente_socket.connect(("127.0.0.1" , 65432))
#Enviar mensaje
cliente_socket.sendall("Hola servidor, me oyes?".encode())
#Recibir respuesta
data = cliente_socket.recv(1024).decode()
print(f"Servidor dice:{data}")
#Cerrar conexion
cliente_socket.close()