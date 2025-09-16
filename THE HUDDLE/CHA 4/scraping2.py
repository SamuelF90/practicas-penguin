# ------------------------------
# SCRAPER COMPLETO: Books To Scrape
# ------------------------------

import time
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ------------------------------
# CONFIGURACIÓN
# ------------------------------
URL_BASE = "https://books.toscrape.com/"
CABECERAS = {"User-Agent": "Mozilla/5.0 (educational scraping)"}

# Para convertir palabras de rating en número
MAPA_RATING = {"Zero":0, "One":1, "Two":2, "Three":3, "Four":4, "Five":5}

# Sesión para hacer los pedidos al sitio
sesion = requests.Session()
sesion.headers.update(CABECERAS)

# ------------------------------
# FUNCIONES
# ------------------------------

def limpiar_precio(texto):
    """Convierte un texto con símbolo de libra u otros caracteres en float"""
    try:
        return float(re.sub(r"[^0-9.]", "", texto))
    except:
        return None

def obtener_sopa(url, reintentos=3, espera=1.0):
    """Descarga la página y devuelve el HTML procesado por BeautifulSoup"""
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
    """Obtiene todas las categorías de libros"""
    sopa = obtener_sopa(URL_BASE)
    categorias = []
    for enlace in sopa.select("div.side_categories ul li ul li a"):
        nombre = enlace.get_text(strip=True)
        url = urljoin(URL_BASE, enlace.get("href"))
        categorias.append({"nombre": nombre, "url": url})
    return categorias

def recorrer_paginas_categoria(url_categoria, espera=0.8):
    """Devuelve (url, sopa) para cada página dentro de una categoría"""
    url = url_categoria
    while url:
        sopa = obtener_sopa(url)
        yield url, sopa
        boton_siguiente = sopa.select_one("li.next a")
        url = urljoin(url, boton_siguiente["href"]) if boton_siguiente else None
        time.sleep(espera)

def leer_tarjetas_libros(sopa_pagina, url_pagina):
    """Extrae la información básica de los libros desde la lista de la categoría"""
    for tarjeta in sopa_pagina.select("article.product_pod"):
        titulo = tarjeta.h3.a.get("title", "Sin título")

        # Manejo seguro del precio
        precio_texto = tarjeta.select_one(".price_color").get_text(strip=True) if tarjeta.select_one(".price_color") else ""
        precio = limpiar_precio(precio_texto)

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
    """Extrae los detalles completos del libro desde su página individual"""
    sopa = obtener_sopa(url_detalle)

    # Descripción
    desc_tag = sopa.select_one("#product_description ~ p")
    descripcion = desc_tag.get_text(strip=True) if desc_tag else ""

    # Tabla de especificaciones
    datos = {}
    for fila in sopa.select("table.table.table-striped tr"):
        clave = fila.th.get_text(strip=True)
        valor = fila.td.get_text(strip=True)
        datos[clave] = valor

    upc = datos.get("UPC", "")
    precio_sin_imp = limpiar_precio(datos.get("Price (excl. tax)", "0"))
    precio_con_imp = limpiar_precio(datos.get("Price (incl. tax)", "0"))
    impuesto = limpiar_precio(datos.get("Tax", "0"))

    stock_texto = datos.get("Availability", "")
    m = re.search(r"(\d+)", stock_texto)
    stock = int(m.group(1)) if m else None

    # Rating
    palabra_rating = "Zero"
    p = sopa.select_one("p.star-rating")
    if p:
        for c in p.get("class", []):
            if c != "star-rating":
                palabra_rating = c
                break
    rating = MAPA_RATING.get(palabra_rating, 0)

    # Imagen
    img = sopa.select_one("#product_gallery img")
    url_imagen = urljoin(url_detalle, img["src"]) if img else None

    # Categoría (breadcrumb)
    migas = [li.get_text(strip=True) for li in sopa.select(".breadcrumb li")]
    categoria = migas[-2] if len(migas) >= 2 else None

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

def scrapear_todo(espera=0.5):
    """Recorre todas las categorías y libros del sitio"""
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
                })
                time.sleep(espera)
    return resultados

# ------------------------------
# BLOQUE PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("🚀 Iniciando scraping de Books to Scrape...")
    libros = scrapear_todo(espera=0.3)  # Ajustá espera si querés más rápido o más seguro

    print("\n✅ Scraping finalizado.")
    print(f"Se encontraron {len(libros)} libros en total.\n")
