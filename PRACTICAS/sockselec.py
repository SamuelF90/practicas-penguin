#SOCKETS DOCUMENTACION
1  import selectors
2  import socket

# import selectors
# Importa el módulo selectors, que provee una abstracción para multiplexación de E/S (select/epoll/kqueue) para manejar muchos sockets sin threads.
# import socket
#importa el módulo estándar de sockets de Python.
#
#

3  sel = selectors.DefaultSelector()

4  def accept(sock, mask):
5      conn, addr = sock.accept()  # Should be ready  
6      print('accepted', conn, 'from', addr)
7      conn.setblocking(False)
8      sel.register(conn, selectors.EVENT_READ, read)

9  def read(conn, mask):
10     data = conn.recv(1000)  # Should be ready
11     if data:
12         print('echoing', repr(data), 'to', conn)
13         conn.send(data)  # Hope it won't block
14     else:
15         print('closing', conn)
16         sel.unregister(conn)
17         conn.close()

18 sock = socket.socket()
19 sock.bind(('localhost', 1234))
20 sock.listen(100)
21 sock.setblocking(False)
22 sel.register(sock, selectors.EVENT_READ, accept)

23 while True:
24     events = sel.select()
25     for key, mask in events:
26         callback = key.data
27         callback(key.fileobj, mask)
