import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

from flask import Flask, Response, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)

with (BASE_DIR / "catalogo.json").open(encoding="utf-8") as catalog_file:
    raw_products = json.load(catalog_file)


def category_for(title):
    name = title.casefold()
    if "café" in name or "cafetto" in name:
        return "Café"
    if "cacao" in name or "chocolate" in name or "nibs" in name:
        return "Cacao"
    if "miel" in name or "uchuva" in name:
        return "Miel y frutas"
    return "Despensa"


PRODUCTS = [
    {
        **product,
        "id": str(index),
        "categoria": category_for(product["titulo"]),
        "image_url": f"/static/img/catalogo/{quote(product['imagen'])}",
    }
    for index, product in enumerate(raw_products, start=1)
]

PAGES = {
    "home": {
        "title": "Nutricol Foods | Alimentos colombianos para nuevos mercados",
        "description": "Conectamos productos de la despensa colombiana con importadores, distribuidores y cadenas comerciales. Origen en Antioquia, visión internacional.",
    },
    "nosotros": {
        "title": "Nosotros | Nutricol Foods",
        "description": "Conoce a Nutricol Foods: una conexión entre el origen alimentario de Antioquia y las oportunidades comerciales en nuevos mercados.",
    },
    "mercados": {
        "title": "Mercados | Nutricol Foods",
        "description": "Soluciones de alimentos colombianos para importadores, distribuidores, cadenas comerciales, mercados latinos y foodservice en Estados Unidos y Europa.",
    },
    "servicios": {
        "title": "Servicios B2B | Nutricol Foods",
        "description": "Abastecimiento y distribución B2B, marca privada, co-packing, packs de regalo y apoyo go-to-market para alimentos colombianos.",
    },
    "catalogo": {
        "title": "Catálogo de productos colombianos | Nutricol Foods",
        "description": "Explora café, cacao, miel y productos de despensa colombiana. Selecciona referencias y solicita una cotización B2B por WhatsApp.",
    },
    "contacto": {
        "title": "Contacto comercial | Nutricol Foods",
        "description": "Hablemos de abastecimiento, distribución o marca privada. Contacta a Nutricol Foods por WhatsApp para explorar una oportunidad B2B.",
    },
    "404": {
        "title": "Página no encontrada | Nutricol Foods",
        "description": "La página que buscas no está disponible. Explora Nutricol Foods y descubre nuestros productos colombianos.",
    },
}


@app.context_processor
def common_context():
    page = request.endpoint if request.endpoint in PAGES else "404"
    canonical = request.url_root.rstrip("/") + request.path
    return {
        "page": page,
        "seo": PAGES[page],
        "canonical": canonical,
        "current_year": datetime.now().year,
        "products_data": [
            {"id": p["id"], "titulo": p["titulo"], "image_url": p["image_url"]}
            for p in PRODUCTS
        ],
    }


@app.route("/")
def home():
    return render_template("home.html", featured=[PRODUCTS[i] for i in (0, 2, 8, 14)])


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/mercados")
def mercados():
    return render_template("mercados.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", products=PRODUCTS)


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


@app.route("/robots.txt")
def robots():
    sitemap = request.url_root.rstrip("/") + url_for("sitemap")
    return Response(f"User-agent: *\nAllow: /\nSitemap: {sitemap}\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    base = request.url_root.rstrip("/")
    routes = ["home", "nosotros", "mercados", "servicios", "catalogo", "contacto"]
    urls = "".join(
        f"<url><loc>{escape(base + url_for(route))}</loc></url>" for route in routes
    )
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        mimetype="application/xml",
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))