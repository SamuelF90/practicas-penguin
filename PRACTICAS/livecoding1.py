def crear_matriz(f, c): return [['.' for _ in range(c)] for _ in range(f)]
def mostrar(m): print('\n'.join(' '.join(fila) for fila in m), end="\n\n")
def coord_ok(f, c, F, C): return 0 <= f < F and 0 <= c < C

def pedir_coord(texto, F, C):
    while True:
        try:
            f, c = map(int, input(f"{texto}: ").strip().split())
            if coord_ok(f, c, F, C): return f, c
            print("❌ Fuera de rango.")
        except: print("❌ Formato inválido. Usa: fila columna")

def main():
    F, C = int(input("Filas: ")), int(input("Columnas: "))
    m = crear_matriz(F, C)

    print("\n🔲 MATRIZ INICIAL:"); mostrar(m)

    print("📍 INICIO (A)"); fi, ci = pedir_coord("Inicio", F, C); m[fi][ci] = 'A'

    print("🎯 FIN (Z)")
    while True:
        ff, cf = pedir_coord("Fin", F, C)
        if (ff, cf) != (fi, ci): m[ff][cf] = 'Z'; break
        print("❌ No puede ser igual al inicio.")

    try: n = int(input("\n🧱 ¿Cuántos obstáculos?: "))
    except: n = 0

    print("Tipos: 1-Edificio(#), 2-Agua(~), 3-Bloqueado(X)")
    simbolos = {'1': '#', '2': '~', '3': 'X'}

    for i in range(n):
        while True:
            try:
                entrada = input(f"Obs {i+1} (fila col tipo): ").strip().split()
                if len(entrada) != 3: raise ValueError
                f, c, t = int(entrada[0]), int(entrada[1]), entrada[2]
                if not coord_ok(f, c, F, C):
                    print("❌ Fuera de rango.")
                elif t not in simbolos:
                    print("❌ Tipo inválido.")
                elif m[f][c] != '.':
                    print("❌ Celda ocupada.")
                else:
                    m[f][c] = simbolos[t]
                    break
            except:
                print("❌ Entrada inválida. Usa: fila columna tipo")

    print("\n🧩 MATRIZ FINAL:"); mostrar(m)

if __name__ == "__main__": main()


