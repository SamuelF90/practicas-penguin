import tkinter as tk
from tkinter import messagebox
import time
from collections import deque

LIBRE = 0
EDIFICIO = 1
AGUA = 2
BLOQUEADO_TEMP = 3

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
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CiudadGUI:
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
        tk.Button(self.botones, text="Buscar Ruta", command=self.buscar_ruta).grid(row=1, column=2)

        self.dibujar_mapa()

    def set_modo(self, modo):
        self.modo = modo

    def clic_celda(self, event):
        x, y = event.y // self.tamano, event.x // self.tamano
        if self.modo == 'inicio':
            self.inicio = Nodo(x, y)
        elif self.modo == 'fin':
            self.fin = Nodo(x, y)
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
                if self.inicio and self.inicio.x == i and self.inicio.y == j:
                    color = COLORES['inicio']
                if self.fin and self.fin.x == i and self.fin.y == j:
                    color = COLORES['fin']
                if actual and actual.x == i and actual.y == j:
                    color = COLORES['actual']
                self.canvas.create_rectangle(j*self.tamano, i*self.tamano, (j+1)*self.tamano, (i+1)*self.tamano, fill=color, outline='black')

    def es_valido(self, x, y, permitir_agua):
        if 0 <= x < self.filas and 0 <= y < self.columnas:
            celda = self.mapa[x][y]
            return celda == LIBRE or (permitir_agua and celda == AGUA)
        return False

    def buscar_ruta(self):
        if not self.inicio or not self.fin:
            messagebox.showwarning("Advertencia", "Debes definir INICIO y FIN")
            return

        for permitir_agua in [False, True]:
            visitado = [[False]*self.columnas for _ in range(self.filas)]
            padre = [[None]*self.columnas for _ in range(self.filas)]
            q = deque([self.inicio])
            visitado[self.inicio.x][self.inicio.y] = True

            dx = [-1, 1, 0, 0]
            dy = [0, 0, -1, 1]

            while q:
                actual = q.popleft()
                self.dibujar_mapa(visitado, actual)
                self.root.update()
                time.sleep(0.05)

                if actual.x == self.fin.x and actual.y == self.fin.y:
                    ruta = []
                    while actual:
                        ruta.append((actual.x, actual.y))
                        actual = padre[actual.x][actual.y]
                    self.dibujar_mapa(visitado, ruta=set(ruta))
                    return

                for d in range(4):
                    nx, ny = actual.x + dx[d], actual.y + dy[d]
                    if self.es_valido(nx, ny, permitir_agua) and not visitado[nx][ny]:
                        visitado[nx][ny] = True
                        padre[nx][ny] = actual
                        q.append(Nodo(nx, ny))

        messagebox.showinfo("Resultado", "No se encontró ruta válida")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Buscador de Ruta - BFS GUI")
    app = CiudadGUI(root, filas=15, columnas=20, tamano=30)
    root.mainloop()

