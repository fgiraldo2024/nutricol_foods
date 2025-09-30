import os
import smtplib
import ssl
from email.utils import formataddr

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")  # Necesaria para flash messages

# Variables de entorno
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO") or EMAIL_USER  # <- si no hay EMAIL_TO, usa el remitente
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/mercados")
def mercados():
    return render_template("mercados.html")

@app.route("/catalogo")
def Catalogo():
    return render_template("catalogo.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    mensaje = request.form.get("mensaje")
    productos = request.form.get("productos")  # <- Campo extra de productos

    try:
        # Crear el correo
        msg = MIMEMultipart("alternative")  # <- soporta texto y HTML
        msg["Subject"] = f"Nuevo mensaje de {nombre}"
        msg["From"]    = formataddr(("Sitio Nutricol", EMAIL_USER))
        msg["To"]      = EMAIL_TO
        if email:
            msg["Reply-To"] = email

        # ---------- Texto plano ----------
        cuerpo_texto = f"""
📩 Nuevo mensaje desde la web Nutricol Foods

👤 Nombre: {nombre}
📧 Email: {email}

📝 Mensaje:
{mensaje}

🛒 Productos a cotizar:
{productos if productos else 'Ninguno seleccionado'}
"""

        # ---------- HTML enriquecido ----------
        productos_html = ""
        if productos:
            for p in productos.splitlines():
                productos_html += f"<li>{p}</li>"
        else:
            productos_html = "<li>Ninguno seleccionado</li>"

        cuerpo_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color:#2E8B57;">📩 Nuevo mensaje desde la web Nutricol Foods</h2>

            <p><strong>👤 Nombre:</strong> {nombre}</p>
            <p><strong>📧 Email:</strong> {email}</p>

            <h3>📝 Mensaje:</h3>
            <p>{mensaje}</p>

            <h3>🛒 Productos a cotizar:</h3>
            <ul>
              {productos_html}
            </ul>
          </body>
        </html>
        """

        # Adjuntar ambos formatos
        msg.attach(MIMEText(cuerpo_texto, "plain", "utf-8"))
        msg.attach(MIMEText(cuerpo_html, "html", "utf-8"))

        # Conexión TLS robusta (587)
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())

        flash("✅ Tu mensaje ha sido enviado con éxito.", "success")
    except Exception as e:
        print("Error enviando correo:", e)
        flash("❌ Hubo un error al enviar el mensaje. Intenta de nuevo.", "danger")

    return redirect(url_for("contacto"))



if __name__ == "__main__":
    app.run(debug=True)
