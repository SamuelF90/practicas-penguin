
# GPS VISUAL SIMULADOR CON BFS - INTERFAZ LIMPIA Y FLUIDA

import pygame
import sys
from collections import deque

pygame.init()

# Configuraciones generales
TAM_CELDA = 40
FILAS, COLUMNAS = 15, 20
ANCHO, ALTO = COLUMNAS * TAM_CELDA, FILAS * TAM_CELDA + 60

# Colores
COLOR_FONDO = (240, 240, 240)
COLOR_LIBRE = (255, 255, 255)
COLOR_EDIFICIO = (70, 70, 70)
COLOR_AGUA = (100, 180, 255)
COLOR_BLOQUEADO = (200, 50, 50)
COLOR_INICIO = (50, 205, 50)
COLOR_FIN = (255, 69, 0)
COLOR_VISITADO = (255, 255, 153)
COLOR_ACTUAL = (255, 200, 0)
COLOR_RUTA = (0, 0, 0)
COLOR_GPS = (255, 255, 0)

# Terreno
LIBRE, EDIFICIO, AGUA, BLOQUEADO = 0, 1, 2, 3

# Inicializacion
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador GPS BFS")
fuente = pygame.font.SysFont(None, 24)

mapa = [[LIBRE for _ in range(COLUMNAS)] for _ in range(FILAS)]
inicio = None
fin = None
tipo_actual = EDIFICIO


def dibujar_mapa(ruta=None, visitados=None, actual=None):
    pantalla.fill(COLOR_FONDO)
    for i in range(FILAS):
        for j in range(COLUMNAS):
            rect = pygame.Rect(j * TAM_CELDA, i * TAM_CELDA + 60, TAM_CELDA, TAM_CELDA)
            tipo = mapa[i][j]
            color = COLOR_LIBRE
            if tipo == EDIFICIO:
                color = COLOR_EDIFICIO
            elif tipo == AGUA:
                color = COLOR_AGUA
            elif tipo == BLOQUEADO:
                color = COLOR_BLOQUEADO
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, (200, 200, 200), rect, 1)

            if visitados and (i, j) in visitados:
                pygame.draw.rect(pantalla, COLOR_VISITADO, rect)
            if ruta and (i, j) in ruta:
                pygame.draw.rect(pantalla, COLOR_RUTA, rect)
                # GPS guiones
                cx, cy = rect.center
                for offset in range(-10, 15, 6):
                    pygame.draw.line(pantalla, COLOR_GPS, (cx - 10 + offset, cy), (cx - 6 + offset, cy), 2)
            if actual and (i, j) == actual:
                pygame.draw.rect(pantalla, COLOR_ACTUAL, rect)

            if inicio == (i, j):
                pygame.draw.rect(pantalla, COLOR_INICIO, rect)
            if fin == (i, j):
                pygame.draw.rect(pantalla, COLOR_FIN, rect)

    pygame.draw.rect(pantalla, (0, 0, 0), (0, 0, ANCHO, 60))
    pantalla.blit(fuente.render("1=Edificio  2=Agua  3=Bloqueado  Espacio=Buscar  R=Reset", True, (255,255,255)), (10, 20))
    pygame.display.flip()


def bfs():
    if not inicio or not fin:
        return None

    visitado = [[False]*COLUMNAS for _ in range(FILAS)]
    padre = [[None]*COLUMNAS for _ in range(FILAS)]
    q = deque()
    q.append(inicio)
    visitado[inicio[0]][inicio[1]] = True
    dx = [-1,1,0,0]
    dy = [0,0,-1,1]
    visitados_anim = set()

    while q:
        x, y = q.popleft()
        visitados_anim.add((x, y))
        dibujar_mapa(visitados=visitados_anim, actual=(x,y))
        pygame.time.delay(40)

        if (x, y) == fin:
            ruta = []
            while (x, y) != inicio:
                ruta.append((x, y))
                x, y = padre[x][y]
            ruta.append(inicio)
            ruta.reverse()
            return ruta

        for d in range(4):
            nx, ny = x+dx[d], y+dy[d]
            if 0 <= nx < FILAS and 0 <= ny < COLUMNAS and not visitado[nx][ny]:
                if mapa[nx][ny] in [LIBRE, AGUA]:
                    visitado[nx][ny] = True
                    padre[nx][ny] = (x, y)
                    q.append((nx, ny))

    return None


def main():
    global tipo_actual, inicio, fin, mapa
    corriendo = True
    ruta = None
    while corriendo:
        dibujar_mapa(ruta)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corriendo = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    tipo_actual = EDIFICIO
                elif e.key == pygame.K_2:
                    tipo_actual = AGUA
                elif e.key == pygame.K_3:
                    tipo_actual = BLOQUEADO
                elif e.key == pygame.K_r:
                    mapa = [[LIBRE for _ in range(COLUMNAS)] for _ in range(FILAS)]
                    inicio, fin, ruta = None, None, None
                elif e.key == pygame.K_SPACE:
                    ruta = bfs()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                fila = (my - 60) // TAM_CELDA
                col = mx // TAM_CELDA
                if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
                    if e.button == 1:
                        mapa[fila][col] = tipo_actual
                    elif e.button == 3:
                        if not inicio:
                            inicio = (fila, col)
                        elif not fin:
                            fin = (fila, col)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
