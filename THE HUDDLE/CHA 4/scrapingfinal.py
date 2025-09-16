# ------------------------------
# SCRAPER + SQLITE COMPLETO
# ------------------------------

import time
import re
import sqlite3
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import random

# ------------------------------
# CONFIGURACIÓN SCRAPER
# ------------------------------
URL_BASE = "https://books.toscrape.com/"
CABECERAS = {"User-Agent": "Mozilla/5.0 (educational scraping)"}

MAPA_RATING = {"Zero":0, "One":1, "Two":2, "Three":3, "Four":4, "Five":5}

# Sesión requests
sesion = requests.Session()
sesion.headers.update(CABECERAS)

# ------------------------------
# FUNCIONES SCRAPER
# ------------------------------
def obtener_sopa(url, reintentos=3, espera=1.0):
    for intento in range(reintentos):
        try:
            respuesta = sesion.get(url, timeout=20)
            if respuesta.ok:
                return BeautifulSoup(respuesta.text, "html.parser")
        except requests.RequestException as e:
            print(f"⚠️ Error al obtener {url}: {e}")
        time.sleep(espera * (intento + 1))
    raise Exception(f"No se pudo obtener la página después de {reintentos} intentos: {url}")

def obtener_categorias():
    sopa = obtener_sopa(URL_BASE)
    categorias = []
    for enlace in sopa.select("div.side_categories ul li ul li a"):
        nombre = enlace.get_text(strip=True)
        url = urljoin(URL_BASE, enlace.get("href"))
        categorias.append({"nombre": nombre, "url": url})
    return categorias

def recorrer_paginas_categoria(url_categoria, espera=0.8):
    url = url_categoria
    while url:
        sopa = obtener_sopa(url)
        yield url, sopa
        boton_siguiente = sopa.select_one("li.next a")
        url = urljoin(url, boton_siguiente["href"]) if boton_siguiente else None
        time.sleep(espera)

def leer_tarjetas_libros(sopa_pagina, url_pagina):
    for tarjeta in sopa_pagina.select("article.product_pod"):
        titulo = tarjeta.h3.a.get("title", "Sin título")
        precio_texto = tarjeta.select_one(".price_color").get_text(strip=True) if tarjeta.select_one(".price_color") else ""
        try:
            precio = float(precio_texto.replace("£", "").strip())
        except ValueError:
            precio = None
        clases = tarjeta.p.get("class", [])
        palabra_rating = next((c for c in clases if c != "star-rating"), "Zero")
        rating = MAPA_RATING.get(palabra_rating, 0)
        enlace_rel = tarjeta.h3.a.get("href", "")
        url_detalle = urljoin(url_pagina, enlace_rel)
        yield {
            "titulo": titulo,
            "precio": precio,
            "rating": rating,
            "url_detalle": url_detalle,
        }

def leer_detalle_libro(url_detalle):
    sopa = obtener_sopa(url_detalle)
    desc_tag = sopa.select_one("#product_description ~ p")
    descripcion = desc_tag.get_text(strip=True) if desc_tag else ""
    datos = {}
    for fila in sopa.select("table.table.table-striped tr"):
        clave = fila.th.get_text(strip=True)
        valor = fila.td.get_text(strip=True)
        datos[clave] = valor
    upc = datos.get("UPC", "")
    try: precio_sin_imp = float(datos.get("Price (excl. tax)", "£0").replace("£",""))
    except: precio_sin_imp=None
    try: precio_con_imp = float(datos.get("Price (incl. tax)", "£0").replace("£",""))
    except: precio_con_imp=None
    try: impuesto = float(datos.get("Tax", "£0").replace("£",""))
    except: impuesto=None
    stock_texto = datos.get("Availability","")
    m = re.search(r"(\d+)", stock_texto)
    stock = int(m.group(1)) if m else None
    palabra_rating = "Zero"
    p = sopa.select_one("p.star-rating")
    if p:
        for c in p.get("class", []):
            if c != "star-rating":
                palabra_rating = c
                break
    rating = MAPA_RATING.get(palabra_rating, 0)
    img = sopa.select_one("#product_gallery img")
    url_imagen = urljoin(url_detalle, img["src"]) if img else None
    migas = [li.get_text(strip=True) for li in sopa.select(".breadcrumb li")]
    categoria = migas[-2] if len(migas)>=2 else None
    return {
        "upc": upc,
        "precio_sin_impuesto": precio_sin_imp,
        "precio_con_impuesto": precio_con_imp,
        "impuesto": impuesto,
        "stock_texto": stock_texto,
        "stock": stock,
        "descripcion": descripcion,
        "rating": rating,
        "url_imagen": url_imagen,
        "categoria_detalle": categoria,
    }

def scrapear_todo(espera=0.3):
    resultados = []
    vistos = set()
    categorias = obtener_categorias()
    for cat in categorias:
        print(f"📚 Categoría: {cat['nombre']}")
        for url_pagina, sopa in recorrer_paginas_categoria(cat["url"], espera=espera):
            for libro in leer_tarjetas_libros(sopa, url_pagina):
                try:
                    detalle = leer_detalle_libro(libro["url_detalle"])
                except Exception as e:
                    print(f"⚠️ Error al leer detalle de {libro['titulo']}: {e}")
                    continue
                if detalle["upc"] in vistos:
                    continue
                vistos.add(detalle["upc"])
                categoria_final = detalle["categoria_detalle"] or cat["nombre"]
                resultados.append({
                    "categoria": categoria_final,
                    "titulo": libro["titulo"],
                    "precio": libro["precio"],
                    "rating": libro["rating"],
                    "upc": detalle["upc"],
                    "descripcion": detalle["descripcion"],
                    "precio_sin_impuesto": detalle["precio_sin_impuesto"],
                    "precio_con_impuesto": detalle["precio_con_impuesto"],
                    "impuesto": detalle["impuesto"],
                    "stock": detalle["stock"],
                    "url_imagen": detalle["url_imagen"],
                    "url": libro["url_detalle"],
                    # Generamos un autor ficticio
                    "autor": f"Autor {random.randint(1,100)}"
                })
                time.sleep(espera)
    return resultados

# ------------------------------
# FUNCIONES BASE DE DATOS
# ------------------------------

def crear_bd(nombre="books.db"):
    conn = sqlite3.connect(nombre)
    cursor = conn.cursor()
    # Crear tablas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Autores (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        precio REAL,
        rating INTEGER,
        upc TEXT UNIQUE,
        descripcion TEXT,
        precio_sin_impuesto REAL,
        precio_con_impuesto REAL,
        impuesto REAL,
        stock INTEGER,
        url_imagen TEXT,
        url TEXT,
        categoria TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Libros_Autores (
        libro_id INTEGER,
        autor_id INTEGER,
        PRIMARY KEY(libro_id, autor_id),
        FOREIGN KEY(libro_id) REFERENCES Libros(id),
        FOREIGN KEY(autor_id) REFERENCES Autores(id)
    )
    """)
    conn.commit()
    return conn

def insertar_libros_autores(conn, libros):
    cursor = conn.cursor()
    for libro in libros:
        # Insertar autor
        cursor.execute("INSERT OR IGNORE INTO Autores(nombre) VALUES (?)", (libro["autor"],))
        cursor.execute("SELECT id FROM Autores WHERE nombre = ?", (libro["autor"],))
        autor_id = cursor.fetchone()[0]
        # Insertar libro
        cursor.execute("""
        INSERT OR IGNORE INTO Libros(titulo, precio, rating, upc, descripcion, precio_sin_impuesto,
        precio_con_impuesto, impuesto, stock, url_imagen, url, categoria)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            libro["titulo"], libro["precio"], libro["rating"], libro["upc"], libro["descripcion"],
            libro["precio_sin_impuesto"], libro["precio_con_impuesto"], libro["impuesto"],
            libro["stock"], libro["url_imagen"], libro["url"], libro["categoria"]
        ))
        cursor.execute("SELECT id FROM Libros WHERE upc=?", (libro["upc"],))
        libro_id = cursor.fetchone()[0]
        # Relación libro-autor
        cursor.execute("INSERT OR IGNORE INTO Libros_Autores(libro_id, autor_id) VALUES (?,?)",
                       (libro_id, autor_id))
    conn.commit()

# ------------------------------
# BLOQUE PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("🚀 Iniciando scraping de Books to Scrape...")
    libros = scrapear_todo(espera=0.3)
    print("\n✅ Scraping finalizado.")
    print(f"Se encontraron {len(libros)} libros en total.\n")

    print("💾 Creando base de datos y guardando libros...")
    conn = crear_bd()
    insertar_libros_autores(conn, libros)
    print("✅ Datos guardados en SQLite!")

    # ------------------------------
    # CONSULTAS DE EJEMPLO
    # ------------------------------
    cursor = conn.cursor()
    print("\n📊 Ejemplo consultas emocionales:")

    # Libros >3 estrellas y < £10
    print("\n1️⃣ Libros >3 estrellas y precio < £10:")
    for row in cursor.execute("SELECT titulo, precio, rating FROM Libros WHERE rating>3 AND precio<10 LIMIT 5"):
        print(row)

    # Libros por autor ficticio
    print("\n2️⃣ Libros por Autor 1:")
    for row in cursor.execute("""
    SELECT l.titulo, a.nombre FROM Libros l
    JOIN Libros_Autores la ON l.id=la.libro_id
    JOIN Autores a ON a.id=la.autor_id
    WHERE a.nombre='Autor 1' LIMIT 5
    """):
        print(row)

    # Libros por categoría
    print("\n3️⃣ Libros de la categoría Travel:")
    for row in cursor.execute("SELECT titulo, categoria FROM Libros WHERE categoria='Travel' LIMIT 5"):
        print(row)

    # Consulta lenta simulada
    print("\n4️⃣ Consulta lenta (sin índice):")
    import time
    start = time.time()
    cursor.execute("SELECT * FROM Libros WHERE precio>0 ORDER BY titulo")
    cursor.fetchall()
    print("Tiempo:", round(time.time()-start, 3), "seg")

    # Crear índice para acelerar
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_precio ON Libros(precio)")
    conn.commit()
    print("\n5️⃣ Consulta rápida (con índice):")
    start = time.time()
    cursor.execute("SELECT * FROM Libros WHERE precio>0 ORDER BY titulo")
    cursor.fetchall()
    print("Tiempo:", round(time.time()-start, 3), "seg")

    conn.close()
    print("\n🎉 Todo listo. Scraper + SQLite + consultas ejecutables.")
