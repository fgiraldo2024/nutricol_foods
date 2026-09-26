import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import PRODUCTS, app  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize("path", ["/", "/nosotros", "/mercados", "/servicios", "/catalogo", "/contacto"])
def test_pages_render_with_metadata(client, path):
    response = client.get(path)
    content = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "<title>" in content
    assert '<meta name="description"' in content
    assert '<link rel="canonical"' in content
    assert 'property="og:title"' in content
    assert '"@type": "Organization"' in content
    assert 'id="main"' in content


def test_catalog_is_server_rendered_and_has_quote_controls(client):
    content = client.get("/catalogo").get_data(as_text=True)
    assert len(PRODUCTS) == 16
    for product in PRODUCTS:
        assert product["titulo"] in content
        assert product["imagen"] in content
        assert f'data-add-product="{product["id"]}"' in content


def test_unique_titles(client):
    paths = ["/", "/nosotros", "/mercados", "/servicios", "/catalogo", "/contacto"]
    titles = []
    for path in paths:
        html = client.get(path).get_data(as_text=True)
        titles.append(html.split("<title>")[1].split("</title>")[0])
    assert len(set(titles)) == len(paths)


def test_sitemap_and_robots(client):
    sitemap = client.get("/sitemap.xml")
    robots = client.get("/robots.txt")
    assert sitemap.status_code == 200
    assert sitemap.mimetype == "application/xml"
    assert sitemap.get_data(as_text=True).count("<loc>") == 6
    assert "Sitemap: http://localhost/sitemap.xml" in robots.get_data(as_text=True)


def test_404_is_styled(client):
    response = client.get("/ruta-inexistente")
    assert response.status_code == 404
    assert "Este camino no lleva" in response.get_data(as_text=True)


def test_catalog_matches_source():
    source = json.loads((Path(__file__).resolve().parents[1] / "catalogo.json").read_text(encoding="utf-8"))
    assert len(PRODUCTS) == len(source)