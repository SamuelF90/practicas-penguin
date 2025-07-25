
import tkinter as tk
from tkinter import messagebox
import time
import heapq

LIBRE = 0
EDIFICIO = 1
AGUA = 2
BLOQUEADO_TEMP = 3

COSTO_LIBRE = 1
COSTO_AGUA = 3
COSTO_BLOQUEADO = 5

COLORES = {
    LIBRE: 'white',
    EDIFICIO: 'brown',
    AGUA: 'blue',
    BLOQUEADO_TEMP: 'red',
    'inicio': 'green',
    'fin': 'gold',
    'visitado': 'purple',
    'camino': 'black',
    'actual': 'orange'
}

class Nodo:
    def __init__(self, x, y, costo):
        self.x = x
        self.y = y
        self.costo = costo

    def __lt__(self, other):
        return self.costo < other.costo

class CiudadDijkstraGUI:
    def __init__(self, root, filas=10, columnas=10, tamano=30):
        self.root = root
        self.filas = filas
        self.columnas = columnas
        self.tamano = tamano
        self.mapa = [[LIBRE for _ in range(columnas)] for _ in range(filas)]
        self.inicio = None
        self.fin = None
        self.canvas = tk.Canvas(root, width=columnas*tamano, height=filas*tamano)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic_celda)
        self.modo = LIBRE

        self.botones = tk.Frame(root)
        self.botones.pack()
        for i, (nombre, tipo) in enumerate({"LIBRE": LIBRE, "EDIFICIO": EDIFICIO, "AGUA": AGUA, "BLOQUEADO": BLOQUEADO_TEMP}.items()):
            tk.Button(self.botones, text=nombre, bg=COLORES[tipo], command=lambda t=tipo: self.set_modo(t)).grid(row=0, column=i)

        tk.Button(self.botones, text="Inicio", bg=COLORES['inicio'], command=lambda: self.set_modo('inicio')).grid(row=1, column=0)
        tk.Button(self.botones, text="Fin", bg=COLORES['fin'], command=lambda: self.set_modo('fin')).grid(row=1, column=1)
        tk.Button(self.botones, text="Buscar Ruta (Dijkstra)", command=self.buscar_ruta_dijkstra).grid(row=1, column=2)

        self.dibujar_mapa()

    def set_modo(self, modo):
        self.modo = modo

    def clic_celda(self, event):
        x, y = event.y // self.tamano, event.x // self.tamano
        if self.modo == 'inicio':
            self.inicio = (x, y)
        elif self.modo == 'fin':
            self.fin = (x, y)
        else:
            self.mapa[x][y] = self.modo
        self.dibujar_mapa()

    def dibujar_mapa(self, visitado=None, actual=None, ruta=None):
        self.canvas.delete("all")
        for i in range(self.filas):
            for j in range(self.columnas):
                color = COLORES[self.mapa[i][j]]
                if visitado and visitado[i][j]:
                    color = COLORES['visitado']
                if ruta and (i, j) in ruta:
                    color = COLORES['camino']
                if self.inicio and self.inicio == (i, j):
                    color = COLORES['inicio']
                if self.fin and self.fin == (i, j):
                    color = COLORES['fin']
                if actual and (i, j) == actual:
                    color = COLORES['actual']
                self.canvas.create_rectangle(j*self.tamano, i*self.tamano, (j+1)*self.tamano, (i+1)*self.tamano, fill=color, outline='black')

    def obtener_costo(self, tipo):
        if tipo == LIBRE:
            return COSTO_LIBRE
        elif tipo == AGUA:
            return COSTO_AGUA
        elif tipo == BLOQUEADO_TEMP:
            return COSTO_BLOQUEADO
        else:
            return float('inf')

    def es_valido(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.mapa[x][y] != EDIFICIO

    def buscar_ruta_dijkstra(self):
        if not self.inicio or not self.fin:
            messagebox.showwarning("Advertencia", "Debes definir INICIO y FIN")
            return

        distancia = [[float('inf')]*self.columnas for _ in range(self.filas)]
        padre = [[None]*self.columnas for _ in range(self.filas)]
        visitado = [[False]*self.columnas for _ in range(self.filas)]
        pq = [Nodo(self.inicio[0], self.inicio[1], 0)]
        distancia[self.inicio[0]][self.inicio[1]] = 0

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        while pq:
            actual = heapq.heappop(pq)
            if visitado[actual.x][actual.y]:
                continue
            visitado[actual.x][actual.y] = True
            self.dibujar_mapa(visitado, (actual.x, actual.y))
            self.root.update()
            time.sleep(0.05)

            if (actual.x, actual.y) == self.fin:
                ruta = []
                nodo = self.fin
                while nodo:
                    ruta.append(nodo)
                    nodo = padre[nodo[0]][nodo[1]]
                self.dibujar_mapa(visitado, ruta=set(ruta))
                return

            for d in range(4):
                nx, ny = actual.x + dx[d], actual.y + dy[d]
                if self.es_valido(nx, ny):
                    nuevo_costo = distancia[actual.x][actual.y] + self.obtener_costo(self.mapa[nx][ny])
                    if nuevo_costo < distancia[nx][ny]:
                        distancia[nx][ny] = nuevo_costo
                        padre[nx][ny] = (actual.x, actual.y)
                        heapq.heappush(pq, Nodo(nx, ny, nuevo_costo))

        messagebox.showinfo("Resultado", "No se encontró ruta válida")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Buscador de Ruta - Dijkstra GUI")
    app = CiudadDijkstraGUI(root, filas=15, columnas=20, tamano=30)
    root.mainloop()
