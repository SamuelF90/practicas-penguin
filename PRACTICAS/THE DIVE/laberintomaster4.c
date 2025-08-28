#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define PARED '#'
#define CAMINO ' '
#define ENTRADA 'E'
#define SALIDA 'S'
#define VISITADO '.'
#define SOLUCION '$'

typedef struct {
    int filas, columnas;
    char **celdas;
} Laberinto;

typedef struct {
    int x, y;
} Posicion;

int operaciones_resolucion = 0;

double obtenerTiempo() {
    return (double)clock() / CLOCKS_PER_SEC;
}

Laberinto* crearLaberinto(int filas, int columnas) {
    Laberinto *lab = malloc(sizeof(Laberinto));
    lab->filas = filas;
    lab->columnas = columnas;
    lab->celdas = malloc(filas * sizeof(char*));
    for (int i = 0; i < filas; i++) {
        lab->celdas[i] = malloc(columnas * sizeof(char));
        for (int j = 0; j < columnas; j++) {
            lab->celdas[i][j] = PARED;
        }
    }
    return lab;
}

Laberinto* copiarLaberinto(Laberinto *original) {
    Laberinto *copia = crearLaberinto(original->filas, original->columnas);
    for (int i = 0; i < original->filas; i++) {
        for (int j = 0; j < original->columnas; j++) {
            copia->celdas[i][j] = original->celdas[i][j];
        }
    }
    return copia;
}

void liberarLaberinto(Laberinto *lab) {
    for (int i = 0; i < lab->filas; i++) {
        free(lab->celdas[i]);
    }
    free(lab->celdas);
    free(lab);
}

void imprimirLaberinto(Laberinto *lab, const char* titulo) {
    printf("\n");
    printf("================================================\n");
    printf("    %s\n", titulo);
    printf("================================================\n");
    
    printf("  ");
    for (int j = 0; j < lab->columnas; j++) {
        printf("--");
    }
    printf("\n");
    
    for (int i = 0; i < lab->filas; i++) {
        printf("| ");
        for (int j = 0; j < lab->columnas; j++) {
            printf("%c ", lab->celdas[i][j]);
        }
        printf("|\n");
    }
    
    printf("  ");
    for (int j = 0; j < lab->columnas; j++) {
        printf("--");
    }
    printf("\n");
}

void barajar(int arr[4][2]) {
    for (int i = 3; i > 0; i--) {
        int r = rand() % (i + 1);
        int tmp0 = arr[i][0];
        int tmp1 = arr[i][1];
        arr[i][0] = arr[r][0];
        arr[i][1] = arr[r][1];
        arr[r][0] = tmp0;
        arr[r][1] = tmp1;
    }
}

void generarLaberinto(Laberinto *lab, int x, int y) {
    lab->celdas[x][y] = CAMINO;

    int direcciones[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    barajar(direcciones);

    for (int i = 0; i < 4; i++) {
        int nx = x + 2 * direcciones[i][0];
        int ny = y + 2 * direcciones[i][1];

        if (nx > 0 && nx < lab->filas - 1 && 
            ny > 0 && ny < lab->columnas - 1 && 
            lab->celdas[nx][ny] == PARED) {
            
            lab->celdas[x + direcciones[i][0]][y + direcciones[i][1]] = CAMINO;
            generarLaberinto(lab, nx, ny);
        }
    }
}

int resolverLaberinto(Laberinto *lab, Posicion actual, Posicion salida) {
    operaciones_resolucion++;

    if (actual.x == salida.x && actual.y == salida.y) {
        lab->celdas[actual.x][actual.y] = SOLUCION;
        return 1;
    }

    if (actual.x < 0 || actual.x >= lab->filas || 
        actual.y < 0 || actual.y >= lab->columnas) {
        return 0;
    }

    if (lab->celdas[actual.x][actual.y] != CAMINO && 
        lab->celdas[actual.x][actual.y] != ENTRADA &&
        lab->celdas[actual.x][actual.y] != SALIDA) {
        return 0;
    }

    char celda_original = lab->celdas[actual.x][actual.y];
    if (celda_original != ENTRADA && celda_original != SALIDA) {
        lab->celdas[actual.x][actual.y] = VISITADO;
    }

    Posicion movimientos[4] = {
        {actual.x + 1, actual.y},
        {actual.x - 1, actual.y},
        {actual.x, actual.y + 1},
        {actual.x, actual.y - 1}
    };

    for (int i = 0; i < 4; i++) {
        if (resolverLaberinto(lab, movimientos[i], salida)) {
            if (celda_original != ENTRADA && celda_original != SALIDA) {
                lab->celdas[actual.x][actual.y] = SOLUCION;
            }
            return 1;
        }
    }

    if (celda_original != ENTRADA && celda_original != SALIDA) {
        lab->celdas[actual.x][actual.y] = celda_original;
    }
    return 0;
}

int main() {
    srand(time(NULL)); //  para que la generación del laberinto sea aleatoria
    int filas, columnas;

    printf("*** GENERADOR Y SOLUCIONADOR  DE LABERINTOS ***\n");
    printf("==========================================\n");

    do {
        printf("Ingrese filas y columnas impares >= 5 (ej. 11 11): ");
        scanf("%d %d", &filas, &columnas);
        
        if (filas < 5 || columnas < 5) {
            printf("ERROR: Las dimensiones deben ser >= 5\n");
        } else if (filas % 2 == 0 || columnas % 2 == 0) {
            printf("ERROR: Las dimensiones deben ser impares\n");
        }
    } while (filas < 5 || columnas < 5 || filas % 2 == 0 || columnas % 2 == 0);

    Laberinto *labInicial = crearLaberinto(filas, columnas);
    imprimirLaberinto(labInicial, "LABERINTO INICIAL (Solo paredes)");

    printf("Presiona Enter para generar el laberinto...");
    getchar();
    getchar();

    printf(">> Generando laberinto...\n");

    clock_t inicioGen = clock();
    Posicion entrada = {1, 1};
    Posicion salida = {filas - 2, columnas - 2};
    generarLaberinto(labInicial, entrada.x, entrada.y);
    labInicial->celdas[entrada.x][entrada.y] = ENTRADA;
    labInicial->celdas[salida.x][salida.y] = SALIDA;
    clock_t finGen = clock();
    double tiempoGen = ((double)(finGen - inicioGen)) / CLOCKS_PER_SEC;

    imprimirLaberinto(labInicial, "LABERINTO GENERADO");
    printf("TIEMPO de generacion: %.6f segundos\n", tiempoGen);

    printf("Presiona Enter para resolver el laberinto...");
    getchar();

    Laberinto *labSolucion = copiarLaberinto(labInicial);
    printf(">> Resolviendo laberinto...\n");

    operaciones_resolucion = 0;
    clock_t inicioRes = clock();
    int solucion = resolverLaberinto(labSolucion, entrada, salida);
    clock_t finRes = clock();

    double tiempoRes = ((double)(finRes - inicioRes)) / CLOCKS_PER_SEC;
    double tiempoMs = tiempoRes * 1000.0;

    if (solucion) {
        labSolucion->celdas[entrada.x][entrada.y] = ENTRADA;
        labSolucion->celdas[salida.x][salida.y] = SALIDA;

        imprimirLaberinto(labSolucion, "LABERINTO RESUELTO (Camino marcado con *)");
        printf(">> SOLUCION ENCONTRADA!\n");
        printf("TIEMPO de resolucion: %.6f segundos (%.3f milisegundos)\n", tiempoRes, tiempoMs);
        printf("OPERACIONES realizadas: %d\n", operaciones_resolucion);

        int celdas_solucion = 0;
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                if (labSolucion->celdas[i][j] == SOLUCION) {
                    celdas_solucion++;
                }
            }
        }
        printf("LONGITUD del camino: %d pasos\n", celdas_solucion + 2);
    } else {
        printf(">> No se encontro solucion al laberinto.\n");
        printf("TIEMPO de busqueda: %.6f segundos (%.3f milisegundos)\n", tiempoRes, tiempoMs);
        printf("OPERACIONES realizadas: %d\n", operaciones_resolucion);
    }

    liberarLaberinto(labInicial);
    liberarLaberinto(labSolucion);

    printf("\n>> Programa terminado exitosamente!\n");
    return 0;
}

