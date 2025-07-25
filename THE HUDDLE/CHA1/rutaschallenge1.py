#CODIGO C++ A PYTHON 

import os
import time
from collections import deque
from enum import Enum

# Tipos de terreno
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

# Clase Ciudad
class Ciudad:
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
                    if tipo == Terreno.LIBRE.value:
                        print('. ', end='')
                    elif tipo == Terreno.EDIFICIO.value:
                        print('# ', end='')
                    elif tipo == Terreno.AGUA.value:
                        print('~ ', end='')
                    elif tipo == Terreno.BLOQUEADO_TEMP.value:
                        print('X ', end='')
            print()

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

    def buscar_ruta_animada(self, permitir_agua=False):
        visitado = [[False for _ in range(self.columnas)] for _ in range(self.filas)]
        padre = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        q = deque()
        q.append(self.inicio)
        visitado[self.inicio.x][self.inicio.y] = True

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        while q:
            actual = q.popleft()

            # Visualización
            visual = [['' for _ in range(self.columnas)] for _ in range(self.filas)]
            for i in range(self.filas):
                for j in range(self.columnas):
                    if i == actual.x and j == actual.y:
                        visual[i][j] = 'O'
                    elif visitado[i][j]:
                        visual[i][j] = '.'
                    else:
                        tipo = self.mapa[i][j]
                        if tipo == Terreno.LIBRE.value:
                            visual[i][j] = '.'
                        elif tipo == Terreno.EDIFICIO.value:
                            visual[i][j] = '#'
                        elif tipo == Terreno.AGUA.value:
                            visual[i][j] = '~'
                        elif tipo == Terreno.BLOQUEADO_TEMP.value:
                            visual[i][j] = 'X'
            visual[self.inicio.x][self.inicio.y] = 'A'
            visual[self.fin.x][self.fin.y] = 'Z'

            os.system('cls' if os.name == 'nt' else 'clear')
            self.imprimir_mapa(visual)
            time.sleep(0.1)

            if actual.x == self.fin.x and actual.y == self.fin.y:
                return self.reconstruir_ruta(padre)

            for d in range(4):
                nx = actual.x + dx[d]
                ny = actual.y + dy[d]
                if self.es_valido(nx, ny) and not visitado[nx][ny]:
                    if self.mapa[nx][ny] == Terreno.LIBRE.value or (permitir_agua and self.mapa[nx][ny] == Terreno.AGUA.value):
                        visitado[nx][ny] = True
                        padre[nx][ny] = actual
                        q.append(Nodo(nx, ny))
        return []

    def reconstruir_ruta(self, padre):
        ruta = []
        actual = self.fin
        while not (actual.x == self.inicio.x and actual.y == self.inicio.y):
            ruta.append(actual)
            actual = padre[actual.x][actual.y]
        ruta.append(self.inicio)
        ruta.reverse()
        return ruta

    def mostrar_ruta_final(self, ruta):
        visual = [['' for _ in range(self.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                tipo = self.mapa[i][j]
                if tipo == Terreno.LIBRE.value:
                    visual[i][j] = '.'
                elif tipo == Terreno.EDIFICIO.value:
                    visual[i][j] = '#'
                elif tipo == Terreno.AGUA.value:
                    visual[i][j] = '~'
                elif tipo == Terreno.BLOQUEADO_TEMP.value:
                    visual[i][j] = 'X'
        for p in ruta:
            if (p.x, p.y) != (self.inicio.x, self.inicio.y) and (p.x, p.y) != (self.fin.x, self.fin.y):
                visual[p.x][p.y] = 'o'
        visual[self.inicio.x][self.inicio.y] = 'A'
        visual[self.fin.x][self.fin.y] = 'Z'
        self.imprimir_mapa(visual)

    def es_valido(self, x, y, ignorar_bloqueo=False):
        if x < 0 or x >= self.filas or y < 0 or y >= self.columnas:
            return False
        celda = self.mapa[x][y]
        if ignorar_bloqueo:
            return True
        return celda != Terreno.EDIFICIO.value and celda != Terreno.BLOQUEADO_TEMP.value

# Función principal
def main():
    f, c = map(int, input("Tamaño del mapa (filas columnas): ").split())
    ciudad = Ciudad(f, c)

    obs = int(input("\nCantidad de obstáculos: "))
    for i in range(obs):
        x, y, tipo = map(int, input(f"Obstáculo {i+1} - Coordenadas (x y) y tipo [1=Edificio, 2=Agua, 3=Bloqueado]: ").split())
        ciudad.configurar_terreno(x, y, tipo)

    ix, iy = map(int, input("\nIngrese coordenadas de INICIO (x y): ").split())
    ciudad.set_inicio(ix, iy)

    fx, fy = map(int, input("Ingrese coordenadas de FIN (x y): ").split())
    ciudad.set_fin(fx, fy)

    print("\nBuscando ruta...\n")
    ruta = ciudad.buscar_ruta_animada(permitir_agua=False)

    if not ruta:
        print("\nRuta directa bloqueada. Intentando con AGUA...\n")
        time.sleep(1)
        ruta = ciudad.buscar_ruta_animada(permitir_agua=True)

    if ruta:
        print("\nRuta encontrada:\n")
        ciudad.mostrar_ruta_final(ruta)
        print(f"\nLongitud: {len(ruta) - 1} pasos\n")
    else:
        print("\nNo se encontró ninguna ruta válida.\n")

if __name__ == "__main__":
    main()
