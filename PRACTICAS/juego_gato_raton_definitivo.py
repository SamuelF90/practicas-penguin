
import random
import os
import time

# Tamaño del tablero
FILAS = 10
COLUMNAS = 10
OBSTACULOS_INICIALES = 10
MAX_TURNOS = 50

# Direcciones posibles (incluye diagonales)
DIRECCIONES = {
    "W": (-1, 0), "A": (0, -1), "S": (1, 0), "D": (0, 1),
    "WA": (-1, -1), "WD": (-1, 1), "SA": (1, -1), "SD": (1, 1)
}

# Representaciones
VACIO = "."
OBSTACULO = "#"
GATO = "G"
RATON = "R"

class Tablero:
    def __init__(self):
        self.grid = [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.colocar_obstaculos(OBSTACULOS_INICIALES)

    def colocar_obstaculos(self, cantidad):
        for _ in range(cantidad):
            while True:
                f, c = random.randint(0, FILAS-1), random.randint(0, COLUMNAS-1)
                if self.grid[f][c] == VACIO:
                    self.grid[f][c] = OBSTACULO
                    break

    def agregar_obstaculos_random(self, cantidad):
        self.colocar_obstaculos(cantidad)

    def en_rango(self, f, c):
        return 0 <= f < FILAS and 0 <= c < COLUMNAS

    def esta_libre(self, f, c):
        return self.en_rango(f, c) and self.grid[f][c] == VACIO

    def mostrar(self, pos_gato, pos_raton):
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(FILAS):
            fila = ""
            for j in range(COLUMNAS):
                if (i, j) == pos_gato:
                    fila += GATO
                elif (i, j) == pos_raton:
                    fila += RATON
                else:
                    fila += self.grid[i][j]
            print(fila)
        print()

class Jugador:
    def __init__(self, tablero):
        self.f, self.c = self.posicion_inicial(tablero)

    def posicion_inicial(self, tablero):
        while True:
            f, c = random.randint(0, FILAS-1), random.randint(0, COLUMNAS-1)
            if tablero.esta_libre(f, c):
                return f, c

    def mover(self, tablero):
        while True:
            mov = input("Movimiento (WASD o combinaciones: WA, WD, SA, SD): ").upper()
            if mov in DIRECCIONES:
                df, dc = DIRECCIONES[mov]
                nf, nc = self.f + df, self.c + dc
                if tablero.esta_libre(nf, nc):
                    self.f, self.c = nf, nc
                    break
                else:
                    print("Movimiento inválido o bloqueado por obstáculo.")
            else:
                print("Movimiento no reconocido.")

class IA_Gato:
    def __init__(self, tablero):
        self.f, self.c = self.posicion_inicial(tablero)

    def posicion_inicial(self, tablero):
        while True:
            f, c = random.randint(0, FILAS-1), random.randint(0, COLUMNAS-1)
            if tablero.esta_libre(f, c):
                return f, c

    def mover(self, tablero, pos_raton):
        mejor_valor = float("-inf")
        mejor_mov = (self.f, self.c)
        for df, dc in DIRECCIONES.values():
            nf, nc = self.f + df, self.c + dc
            if tablero.esta_libre(nf, nc) or (nf, nc) == pos_raton:
                valor = self.minimax(tablero, (nf, nc), pos_raton, 2, False)
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_mov = (nf, nc)
        self.f, self.c = mejor_mov

    def minimax(self, tablero, pos_gato, pos_raton, profundidad, es_max):
        if pos_gato == pos_raton:
            return 100 if es_max else -100
        if profundidad == 0:
            return -self.distancia(pos_gato, pos_raton)

        if es_max:
            max_eval = float("-inf")
            for df, dc in DIRECCIONES.values():
                nf, nc = pos_gato[0] + df, pos_gato[1] + dc
                if tablero.esta_libre(nf, nc) or (nf, nc) == pos_raton:
                    eval = self.minimax(tablero, (nf, nc), pos_raton, profundidad-1, False)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for df, dc in DIRECCIONES.values():
                nf, nc = pos_raton[0] + df, pos_raton[1] + dc
                if tablero.esta_libre(nf, nc) or (nf, nc) == pos_gato:
                    eval = self.minimax(tablero, pos_gato, (nf, nc), profundidad-1, True)
                    min_eval = min(min_eval, eval)
            return min_eval

    def distancia(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.jugador = Jugador(self.tablero)
        self.ia = IA_Gato(self.tablero)
        self.turno = 0

    def jugar(self):
        while True:
            self.tablero.mostrar((self.ia.f, self.ia.c), (self.jugador.f, self.jugador.c))
            print(f"Turno {self.turno+1}/{MAX_TURNOS}")

            if (self.ia.f, self.ia.c) == (self.jugador.f, self.jugador.c):
                print("¡El Gato atrapó al Ratón! 🐱🎉")
                break

            if self.turno >= MAX_TURNOS:
                print("¡El Ratón logró escapar tras 50 turnos! 🐭🏁")
                break

            # Movimiento del jugador
            self.jugador.mover(self.tablero)

            # Movimiento del Gato IA
            self.ia.mover(self.tablero, (self.jugador.f, self.jugador.c))

            # Agregar obstáculos aleatorios cada 5 turnos
            if self.turno % 5 == 0 and self.turno != 0:
                self.tablero.agregar_obstaculos_random(2)

            self.turno += 1
            time.sleep(0.5)

if __name__ == "__main__":
    juego = Juego()
    juego.jugar()
