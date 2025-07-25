#LIVECODING SE PASA SI O SI
def matriz(filas,columnas):
    return[['.' for _ in range(columnas)]for _ in range(filas)]

def inicio_fin(mapa,inicio,fin):
    mapa[inicio[0]][inicio[1]] = 'A'
    mapa[fin[0]][fin[1]] = 'Z'

def pos_obs(mapa,obstaculo):
    mapa[obstaculo[0]][obstaculo[1]] = '#'

def mostrar_matriz(mapa):
    for filas in (mapa):
        print(" ".join(filas))

def main():
    filas = int(input("Ingrese Filas:"))
    columnas = int(input("Ingrese Columnas: "))
    mapa = matriz(filas,columnas)
    mostrar_matriz(mapa)
    
    inicio_fil = int(input("Ingrese Filas Inicio: "))
    inicio_col = int(input("Ingrese Columna Inicio"))
    
    fin_fil = int(input("Ingrese Filas de Fin: "))
    fin_col = int(input("Ingrese Columnas de Fin:"))
    
    inicio_t = inicio_fil, inicio_col
    fin_t = fin_fil, fin_col
    
    inicio_fin(mapa,inicio_t,fin_t)
    mostrar_matriz(mapa)
    
    obstaculo_fil = int(input("Ingrese un obstaculo fila: "))
    obstaculo_col = int(input("Ingrese obstaculo columna: "))
    obs = obstaculo_fil, obstaculo_col
    pos_obs(mapa, obs)
    mostrar_matriz(mapa)
    
# if __name__ == "__main__":
main()
    
    
    