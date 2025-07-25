import pygame
import random
import copy
import sys

# Configuraciones
BOARD_SIZE = 8
CELL_SIZE = 60
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
FPS = 10

EMPTY = 0
OBSTACLE = 1
GATO = 2
RATON = 3

# Movimientos en 8 direcciones (arriba, abajo, izquierda, derecha y diagonales)
MOVS = [(-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)]

MAX_TURNS = 50
OBSTACLE_ADD_TURNS = 5  # Cada 5 turnos se agrega un obstáculo nuevo

# Colores
COLOR_BG = (30, 30, 30)
COLOR_GRID = (50, 50, 50)
COLOR_OBSTACLE = (139, 69, 19)  # Marrón para queso/obstáculo
COLOR_GATO = (255, 0, 0)        # Rojo para gato
COLOR_RATON = (0, 255, 0)       # Verde para ratón
COLOR_EMPTY = (200, 200, 200)

def crear_tablero():
    tablero = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # Agregar algunos obstáculos iniciales
    for _ in range(8):
        x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
        # No poner obstáculos en posiciones de inicio
        if (x, y) not in [(0, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]:
            tablero[x][y] = OBSTACLE
    return tablero

def es_valido(x, y, tablero):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and tablero[x][y] != OBSTACLE

def distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def imprimir_tablero_console(tablero):
    for fila in tablero:
        print(" ".join(str(c) for c in fila))
    print()

def agregar_obstaculo(tablero):
    intentos = 0
    while intentos < 50:
        x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
        if tablero[x][y] == EMPTY and (x,y) != (0,0) and (x,y) != (BOARD_SIZE-1, BOARD_SIZE-1):
            tablero[x][y] = OBSTACLE
            break
        intentos += 1

def minimax(tablero, gato, raton, profundidad, max_turno):
    if gato == raton:
        return -9999 if max_turno else 9999
    if profundidad == 0:
        # Evaluación: distancia + penalización por obstáculos cercanos
        return distancia(raton, gato)

    if max_turno:  # turno ratón, quiere maximizar la distancia
        max_eval = -float('inf')
        for dx, dy in MOVS:
            nx, ny = raton[0] + dx, raton[1] + dy
            if es_valido(nx, ny, tablero) and (nx, ny) != gato:
                eval = minimax(tablero, gato, (nx, ny), profundidad-1, False)
                max_eval = max(max_eval, eval)
        return max_eval
    else:  # turno gato, quiere minimizar la distancia
        min_eval = float('inf')
        for dx, dy in MOVS:
            nx, ny = gato[0] + dx, gato[1] + dy
            if es_valido(nx, ny, tablero) and (nx, ny) != raton:
                eval = minimax(tablero, (nx, ny), raton, profundidad-1, True)
                min_eval = min(min_eval, eval)
        return min_eval

def mejor_movimiento(tablero, pos_actual, otro_pos, profundidad, es_raton):
    mejor_valor = -float('inf') if es_raton else float('inf')
    mejor_pos = pos_actual

    for dx, dy in MOVS:
        nx, ny = pos_actual[0] + dx, pos_actual[1] + dy
        if es_valido(nx, ny, tablero) and (nx, ny) != otro_pos:
            valor = minimax(tablero, (nx, ny) if not es_raton else otro_pos,
                            otro_pos if not es_raton else (nx, ny),
                            profundidad-1,
                            not es_raton)
            if es_raton and valor > mejor_valor:
                mejor_valor = valor
                mejor_pos = (nx, ny)
            elif not es_raton and valor < mejor_valor:
                mejor_valor = valor
                mejor_pos = (nx, ny)
    return mejor_pos

def juego_terminado(gato, raton, turnos):
    if gato == raton:
        return "gato"
    if turnos >= MAX_TURNS:
        return "raton"
    return None

def dibujar_tablero(screen, tablero, gato, raton):
    screen.fill(COLOR_BG)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = COLOR_EMPTY
            if tablero[x][y] == OBSTACLE:
                color = COLOR_OBSTACLE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

    # Dibujar gato
    rect_gato = pygame.Rect(gato[1]*CELL_SIZE, gato[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, COLOR_GATO, rect_gato)

    # Dibujar ratón
    rect_raton = pygame.Rect(raton[1]*CELL_SIZE, raton[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, COLOR_RATON, rect_raton)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Lab de Gato y Ratón con Minimax")
    clock = pygame.time.Clock()

    tablero = crear_tablero()
    gato = (0, 0)
    raton = (BOARD_SIZE-1, BOARD_SIZE-1)
    turnos = 0

    # Primero ratón se mueve aleatorio 3 turnos para simular "genio dormido"
    raton_turnos_aleatorios = 3

    font = pygame.font.SysFont(None, 36)
    resultado = None

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if resultado is None:
            # Turno ratón
            if raton_turnos_aleatorios > 0:
                # Movimiento aleatorio válido
                posibles = []
                for dx, dy in MOVS:
                    nx, ny = raton[0] + dx, raton[1] + dy
                    if es_valido(nx, ny, tablero) and (nx, ny) != gato:
                        posibles.append((nx, ny))
                if posibles:
                    raton = random.choice(posibles)
                raton_turnos_aleatorios -= 1
            else:
                raton = mejor_movimiento(tablero, raton, gato, 3, True)

            # Chequear fin
            resultado = juego_terminado(gato, raton, turnos)
            if resultado:
                continue

            # Turno gato
            gato = mejor_movimiento(tablero, gato, raton, 4, False)

            # Cada cierto turnos agregar un obstáculo aleatorio
            if turnos % OBSTACLE_ADD_TURNS == 0 and turnos != 0:
                agregar_obstaculo(tablero)

            # Chequear fin
            resultado = juego_terminado(gato, raton, turnos)

            turnos += 1

        # Dibujar todo
        dibujar_tablero(screen, tablero, gato, raton)

        if resultado == "gato":
            text = font.render("El Gato atrapó al Ratón! 🐱", True, (255, 255, 255))
            screen.blit(text, (10, WINDOW_SIZE//2 - 20))
        elif resultado == "raton":
            text = font.render("El Ratón escapó! 🐭", True, (255, 255, 255))
            screen.blit(text, (10, WINDOW_SIZE//2 - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()