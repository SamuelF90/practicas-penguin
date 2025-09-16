#servidor socket

import socket
#CREAR EL SOCKET (IPv4, TCP)
servidor_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#VINCULAR A IP Y PUERTO
servidor_soket.bind(("127.0.0.1", 65432))
#ESCUCHAR CONEXIONES
servidor_soket.listen()
print("Servidor escuchando en 127.0.0.1:65432....")
#ACEPTAR CONEXIONES
conn,addr = servidor_soket.accept()
print(f"Conetado con{addr}")
#Recibir mensaje
data= conn.recv(1024).decode()
print(f"Cliente dice: {data}")
#Responder 
conn.sendall("Hola cliente, te escucho fuerte y claro".encode())
#Cerrar conexion
conn.close()



