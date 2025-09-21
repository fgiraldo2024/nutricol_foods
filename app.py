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
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/productos")
def productos():
    return render_template("productos.html")


@app.route("/mercados")
def mercados():
    return render_template("mercados.html")


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


@app.route("/enviar", methods=["POST"])
def enviar():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    mensaje = request.form.get("mensaje")

    try:
        # Crear el correo
        msg = MIMEMultipart()
        msg["Subject"] = f"Nuevo mensaje de {nombre}"
        msg["From"]    = formataddr(("Sitio Nutricol", EMAIL_USER))  # From = usuario SMTP
        msg["To"]      = EMAIL_TO
        if email:
            msg["Reply-To"] = email

        cuerpo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"
        msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

        # Conexión TLS robusta (587)
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())

        flash("✅ Tu mensaje ha sido enviado con éxito.", "success")


    return redirect(url_for("contacto"))


if __name__ == "__main__":
    app.run(debug=True)
