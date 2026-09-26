# Nutricol Foods — código del sitio

Sitio web hecho en Python y Flask. Incluye páginas, catálogo de productos, imágenes, estilos y pruebas. El formulario de contacto y las solicitudes de cotización abren WhatsApp para que el visitante revise el mensaje antes de enviarlo.

## Probar en tu computador

Necesitas Python 3.10 o posterior. Descomprime el archivo y ejecuta estos comandos desde la carpeta `nutricol-flask`:

```sh
python -m pip install -r requirements.txt
python app.py
```

Abre `http://localhost:5000` en tu navegador. Para detener el servidor, pulsa `Ctrl+C` en la terminal.

Para ejecutar las pruebas:

```sh
python -m pytest -q tests
```

## Montarlo en un servidor

En un servidor Linux o proveedor compatible con Python, instala las dependencias como se indica arriba y configura este comando de inicio desde la carpeta `nutricol-flask`:

```sh
gunicorn --bind 0.0.0.0:${PORT:-8000} app:app
```

`PORT` es el puerto asignado por el proveedor; si no lo asigna, se usará el 8000. Configura en tu proveedor el dominio y HTTPS para hacer pública la página. Descomprimir este archivo **no publica** el sitio ni cambia el dominio actual.

## Contenido

- `app.py`: aplicación Flask y rutas.
- `catalogo.json`: productos del catálogo.
- `templates/`: páginas HTML.
- `static/`: imágenes, CSS y JavaScript.
- `tests/`: pruebas automatizadas.
- `requirements.txt`: dependencias de Python.