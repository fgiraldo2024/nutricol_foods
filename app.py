import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesaria para flash messages

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
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO
        msg["Subject"] = f"Nuevo mensaje de {nombre}"

        cuerpo = f"""
        Nombre: {nombre}
        Email: {email}
        Mensaje: {mensaje}
        """

        msg.attach(MIMEText(cuerpo, "plain"))

        # Conexión al servidor SMTP de GoDaddy
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())

        flash("✅ Tu mensaje ha sido enviado con éxito.", "success")
    except Exception as e:
        print("Error enviando correo:", e)
        flash("❌ Hubo un error al enviar el mensaje. Intenta de nuevo.", "danger")

    return redirect(url_for("contacto"))


if __name__ == "__main__":
    app.run(debug=True)
