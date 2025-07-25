#JUEGO GATO VS RATON SIMPLEX
import random
import pygame
import sys

# --- CONFIGURACIÓN DEL JUEGO ---

FILAS = 10
COLUMNAS = 12
CELL_SIZE = 60
WIDTH, HEIGHT = COLUMNAS * CELL_SIZE, FILAS * CELL_SIZE
FPS = 5
MAX_TURNOS = 30

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OBSTACULO = (255, 0, 0)
RATON_COLOR = (128, 128, 128)
GATO_COLOR = (255, 165, 0)
BORDER = (0, 0, 0)

# Direcciones de movimiento
MOV_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MOV_8 = MOV_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐭 Ratón vs Gato 🐱")
clock = pygame.time.Clock()

# --- FUNCIONES AUXILIARES ---

def dibujar_tablero(raton, gato, obstaculos):
    ventana.fill(WHITE)
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x = col * CELL_SIZE
            y = fila * CELL_SIZE
            pygame.draw.rect(ventana, BORDER, (x, y, CELL_SIZE, CELL_SIZE), 1)

    for (f, c) in obstaculos:
        pygame.draw.rect(ventana, OBSTACULO, (c * CELL_SIZE, f * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(ventana, GATO_COLOR, (gato[1] * CELL_SIZE, gato[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(ventana, RATON_COLOR, (raton[1] * CELL_SIZE, raton[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

def generar_obstaculos(cantidad, inicio, destino):
    obstaculos = set()
    while len(obstaculos) < cantidad:
        pos = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))
        if pos != inicio and pos != destino:
            obstaculos.add(pos)
    return list(obstaculos)

def es_valida(pos, obstaculos):
    f, c = pos
    return 0 <= f < FILAS and 0 <= c < COLUMNAS and pos not in obstaculos

def mover_aleatorio(pos, obstaculos):
    opciones = []
    for df, dc in MOV_8:
        nueva = (pos[0] + df, pos[1] + dc)
        if es_valida(nueva, obstaculos):
            opciones.append(nueva)
    return random.choice(opciones) if opciones else pos

def mover_ratón_inteligente(raton, gato, obstaculos):
    mejores = []
    max_dist = -1
    for df, dc in MOV_8:
        nueva = (raton[0] + df, raton[1] + dc)
        if es_valida(nueva, obstaculos):
            dist = abs(nueva[0] - gato[0]) + abs(nueva[1] - gato[1])
            if dist > max_dist:
                mejores = [nueva]
                max_dist = dist
            elif dist == max_dist:
                mejores.append(nueva)
    return random.choice(mejores) if mejores else raton

def mover_gato_estrategico(gato, raton, obstaculos):
    mejores = []
    min_dist = float('inf')
    for df, dc in MOV_8:  # usa las 8 direcciones para igualar al ratón
        nueva = (gato[0] + df, gato[1] + dc)
        if es_valida(nueva, obstaculos):
            dist = abs(nueva[0] - raton[0]) + abs(nueva[1] - raton[1])
            if dist < min_dist:
                mejores = [nueva]
                min_dist = dist
            elif dist == min_dist:
                mejores.append(nueva)
    return random.choice(mejores) if mejores else gato

# --- INICIO DEL JUEGO ---

def main():
    raton_pos = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))
    gato_pos = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))

    while gato_pos == raton_pos:
        gato_pos = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))

    obstaculos = generar_obstaculos(20, raton_pos, gato_pos)

    turnos = 0
    modo_inteligente = False

    while turnos < MAX_TURNOS:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not modo_inteligente:
            raton_pos = mover_aleatorio(raton_pos, obstaculos)
            modo_inteligente = True  # solo el primer turno es aleatorio
        else:
            raton_pos = mover_ratón_inteligente(raton_pos, gato_pos, obstaculos)

        if raton_pos == gato_pos:
            print("💀 El gato atrapó al ratón. ¡Fin del juego!")
            break

        gato_pos = mover_gato_estrategico(gato_pos, raton_pos, obstaculos)

        if raton_pos == gato_pos:
            print("💀 El gato atrapó al ratón. ¡Fin del juego!")
            break

        dibujar_tablero(raton_pos, gato_pos, obstaculos)
        clock.tick(FPS)
        turnos += 1

    if raton_pos != gato_pos:
        print("🎉 El ratón escapó tras", MAX_TURNOS, "turnos. ¡Victoria!")

    pygame.quit()

if __name__ == "__main__":
    main()










