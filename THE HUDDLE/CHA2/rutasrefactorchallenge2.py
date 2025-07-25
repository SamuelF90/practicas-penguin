#CODIGO EN CLASES DE PYTHON
import os
import time
from collections import deque
from enum import Enum

# Enum para tipos de terreno
class Terreno(Enum):
    LIBRE = 0
    EDIFICIO = 1
    AGUA = 2
    BLOQUEADO_TEMP = 3

# Nodo para coordenadas
class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Clase que maneja el mapa
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[Terreno.LIBRE.value for _ in range(columnas)] for _ in range(filas)]
        self.inicio = None
        self.fin = None

    def imprimir_mapa(self, visual=None):
        for i in range(self.filas):
            for j in range(self.columnas):
                if visual:
                    print(visual[i][j], end=' ')
                else:
                    tipo = self.mapa[i][j]
                    print(self.simbolo_tipo(tipo), end=' ')
            print()

    def simbolo_tipo(self, tipo):
        return {
            Terreno.LIBRE.value: '.',
            Terreno.EDIFICIO.value: '#',
            Terreno.AGUA.value: '~',
            Terreno.BLOQUEADO_TEMP.value: 'X'
        }.get(tipo, '?')

    def configurar_terreno(self, x, y, tipo):
        if self.es_valido(x, y, ignorar_bloqueo=True):
            self.mapa[x][y] = tipo

    def set_inicio(self, x, y):
        if self.es_valido(x, y):
            self.inicio = Nodo(x, y)
        else:
            print("\nInicio inválido.")

    def set_fin(self, x, y):
        if self.es_valido(x, y):
            self.fin = Nodo(x, y)
        else:
            print("\nDestino inválido.")

    def es_valido(self, x, y, ignorar_bloqueo=False):
        if x < 0 or x >= self.filas or y < 0 or y >= self.columnas:
            return False
        celda = self.mapa[x][y]
        if ignorar_bloqueo:
            return True
        return celda != Terreno.EDIFICIO.value and celda != Terreno.BLOQUEADO_TEMP.value

# Clase que contiene el algoritmo BFS para encontrar rutas
class AlgoritmoResolucion:
    def __init__(self, mapa: Mapa):
        self.mapa = mapa

    def buscar_ruta_animada(self, permitir_agua=False):
        visitado = [[False for _ in range(self.mapa.columnas)] for _ in range(self.mapa.filas)]
        padre = [[None for _ in range(self.mapa.columnas)] for _ in range(self.mapa.filas)]
        q = deque()
        q.append(self.mapa.inicio)
        visitado[self.mapa.inicio.x][self.mapa.inicio.y] = True

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        while q:
            actual = q.popleft()
            self.imprimir_visual(actual, visitado)

            if actual.x == self.mapa.fin.x and actual.y == self.mapa.fin.y:
                return self.reconstruir_ruta(padre)

            for d in range(4):
                nx, ny = actual.x + dx[d], actual.y + dy[d]
                if self.mapa.es_valido(nx, ny) and not visitado[nx][ny]:
                    tipo = self.mapa.mapa[nx][ny]
                    if tipo == Terreno.LIBRE.value or (permitir_agua and tipo == Terreno.AGUA.value):
                        visitado[nx][ny] = True
                        padre[nx][ny] = actual
                        q.append(Nodo(nx, ny))
        return []

    def reconstruir_ruta(self, padre):
        ruta = []
        actual = self.mapa.fin
        while not (actual.x == self.mapa.inicio.x and actual.y == self.mapa.inicio.y):
            ruta.append(actual)
            actual = padre[actual.x][actual.y]
        ruta.append(self.mapa.inicio)
        ruta.reverse()
        return ruta

    def imprimir_visual(self, actual, visitado):
        visual = [['' for _ in range(self.mapa.columnas)] for _ in range(self.mapa.filas)]
        for i in range(self.mapa.filas):
            for j in range(self.mapa.columnas):
                if i == actual.x and j == actual.y:
                    visual[i][j] = 'O'
                elif visitado[i][j]:
                    visual[i][j] = '.'
                else:
                    visual[i][j] = self.mapa.simbolo_tipo(self.mapa.mapa[i][j])
        visual[self.mapa.inicio.x][self.mapa.inicio.y] = 'A'
        visual[self.mapa.fin.x][self.mapa.fin.y] = 'Z'

        os.system('cls' if os.name == 'nt' else 'clear')
        self.mapa.imprimir_mapa(visual)
        time.sleep(0.1)

    def mostrar_ruta_final(self, ruta):
        visual = [['' for _ in range(self.mapa.columnas)] for _ in range(self.mapa.filas)]
        for i in range(self.mapa.filas):
            for j in range(self.mapa.columnas):
                visual[i][j] = self.mapa.simbolo_tipo(self.mapa.mapa[i][j])
        for p in ruta:
            if (p.x, p.y) != (self.mapa.inicio.x, self.mapa.inicio.y) and (p.x, p.y) != (self.mapa.fin.x, self.mapa.fin.y):
                visual[p.x][p.y] = 'o'
        visual[self.mapa.inicio.x][self.mapa.inicio.y] = 'A'
        visual[self.mapa.fin.x][self.mapa.fin.y] = 'Z'
        self.mapa.imprimir_mapa(visual)

# Clase que controla el flujo del juego
class Juego:
    def __init__(self):
        self.mapa = None
        self.algoritmo = None

    def ejecutar(self):
        f, c = map(int, input("Tamaño del mapa (filas columnas): ").split())
        self.mapa = Mapa(f, c)
        self.algoritmo = AlgoritmoResolucion(self.mapa)

        obs = int(input("\nCantidad de obstáculos: "))
        for i in range(obs):
            x, y, tipo = map(int, input(f"Obstáculo {i+1} - Coordenadas (x y) y tipo [1=Edificio, 2=Agua, 3=Bloqueado]: ").split())
            self.mapa.configurar_terreno(x, y, tipo)

        ix, iy = map(int, input("\nIngrese coordenadas de INICIO (x y): ").split())
        self.mapa.set_inicio(ix, iy)

        fx, fy = map(int, input("Ingrese coordenadas de FIN (x y): ").split())
        self.mapa.set_fin(fx, fy)

        print("\nBuscando ruta...\n")
        ruta = self.algoritmo.buscar_ruta_animada(permitir_agua=False)

        if not ruta:
            print("\nRuta directa bloqueada. Intentando con AGUA...\n")
            time.sleep(1)
            ruta = self.algoritmo.buscar_ruta_animada(permitir_agua=True)

        if ruta:
            print("\nRuta encontrada:\n")
            self.algoritmo.mostrar_ruta_final(ruta)
            print(f"\nLongitud: {len(ruta) - 1} pasos\n")
        else:
            print("\nNo se encontró ninguna ruta válida.\n")

# Función principal
def main():
    juego = Juego()
    juego.ejecutar()

if __name__ == "__main__":
    main()
