PASO A PASO – Integración del Catálogo Dinámico (Flask)

Estructura esperada en tu proyecto:
  /tu_app/
    app.py
    /templates/
    /static/

1) Copiar carpetas
   - Copia 'templates/catalogo.html' a tu carpeta templates.
   - Copia 'static/img/catalogo/' completa dentro de tu carpeta static/img/.
   - Copia 'static/data/catalogo.json' dentro de static/data/ (crea la carpeta si no existe).

2) Agregar la ruta en app.py
   Añade esto en tu app Flask:
       @app.route('/catalogo')
       def Catalogo():
           return render_template('catalogo.html')

3) Agregar el link en tu navbar
   En tu plantilla base (base.html/header), agrega:
       <a href="{{ url_for('Catalogo') }}">Catálogo</a>

4) Probar en local
   - Ejecuta: flask run (o python app.py) y abre http://127.0.0.1:5000/catalogo

5) Mantener el catálogo
   - Edita static/data/catalogo.json para agregar/editar productos.
   - Coloca cada imagen nueva en static/img/catalogo y en el JSON usa solo el nombre del archivo.
   - Recomendación: nombres en minúsculas y sin espacios.

Formato JSON de ejemplo:
[
  {"titulo":"Producto X","descripcion":"Breve desc","precio":"$0","imagen":"archivo.jpg"}
]

Si NO usas Flask (HTML estático):
  - Abre templates/catalogo.html y reemplaza:
       const jsonUrl = "{{ url_for('static', filename='data/catalogo.json') }}";
       const imgBase = "{{ url_for('static', filename='img/catalogo/') }}";
    por:
       const jsonUrl = "static/data/catalogo.json";
       const imgBase = "static/img/catalogo/";
