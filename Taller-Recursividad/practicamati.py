# crear una matriz 
def matriz(filas, columnas):
    return [['.' for _ in range(columnas)] for _ in range(filas)]

#Posicionar entrada y salida
def inicio_fin (mapa, inicio, fin):
    mapa[inicio[0]][inicio[1]] = 'E'
    mapa[fin[0]][fin[1]] = 'S'

#colocar obstaculos en la matriz 
def posicion_obstaculos(mapa, obstaculo):
    mapa[obstaculo[0]][obstaculo[1]] = 'X'

def mostrar_matriz(mapa):
    for filas in mapa:
        print(" ".join(filas))
        


# manejar todo dentro del main 
# no hace falta validar siempre y cuando se vea en la matriz 
def main():
    filas = int(input("Ingrese filas:"))
    columnas = int(input("Ingrese columnas:"))
    mapa = matriz(filas, columnas)
    mostrar_matriz(mapa)
    
    inicio_fil = int(input("Ingrese entrada fila:"))
    inicio_col = int(input("Ingrese entrada columna: "))
    salida_fil = int(input("Ingrese salida fila:"))
    salida_col = int(input("Ingrese salida columna:"))
    
    inicio_t = inicio_fil, inicio_col
    salida_t = salida_fil, salida_col
    inicio_fin(mapa, inicio_t, salida_t)
    mostrar_matriz(mapa)
    
    obstaculos_fil = int(input("Ingrese la fila del obs:"))
    obstaculos_col = int(input("Ingrese la columna del obs: "))
    obs = obstaculos_fil, obstaculos_col 
    posicion_obstaculos(mapa, obs)
    mostrar_matriz(mapa)





# para indicar de donde iniciara la ejcucion del proframa 
if __name__ == "__main__":
    main()