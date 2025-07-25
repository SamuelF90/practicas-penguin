def crear_matriz(f, c):
    
    return [['.' for _ in range(c)] for _ in range(f)]

def insertar_obstaculo(matriz, f, c):
    # codigo aqui

def mostrar(m):
    # codigo aqui
    print('\n'.join(' '.join(fila) for fila in m), end="\n\n")
    


def main():
    f = int(input("Filas: "))
    c = int(input("Columnas: "))
    m = crear_matriz(f, c)
    print("Matriz Generada:")
    mostrar(m)

if __name__ == "__main__":
    main()
