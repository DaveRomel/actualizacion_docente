import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path
from schema.inscripcion_schema import NotificacionInscripcionSchema
load_dotenv()
from pydantic import BaseModel
from email.utils import make_msgid
from email.mime.image import MIMEImage

async def send_email(subject: str, data: BaseModel, email: str, template_file: str):
    # Obtener variables del .env y corregir el tipo de datos
    smtp_host = os.getenv("SMTP_HOST_FA")
    smtp_port = int(os.getenv("SMTP_EMAIL_PORT_FA"))  # Convertir puerto a int
    smtp_user = os.getenv("SMTP_EMAIL_USERNAME_FA")
    smtp_password = os.getenv("SMTP_EMAIL_PASSWORD_FA")

    # Generar los CID únicos
    cid_logo = make_msgid(domain="logo")[1:-1]   # eliminar los <>
    cid_fondo = make_msgid(domain="fondo")[1:-1]

    # Cargar el archivo HTML como plantilla
    with open(Path(__file__).parent / template_file, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Reemplazar las variables en el HTML
    html_body = html_template.format(**data.dict(), cid_fondo=cid_fondo, cid_logo = cid_logo)  # Reemplazar la variable nombre en el HTML

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = email  
    message["Subject"] = subject

    # Crear parte alternativa para HTML
    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(MIMEText(html_body, "html", "utf-8"))
    message.attach(msg_alternative)

    # Adjuntar fondo.jpg
    with open(Path(__file__).parent / "fondo.jpg", "rb") as f:
        img_fondo = MIMEImage(f.read())
        img_fondo.add_header("Content-ID", f"<{cid_fondo}>")
        message.attach(img_fondo)

    # Adjuntar logo.jpg
    with open(Path(__file__).parent / "logo.png", "rb") as f:
        img_logo = MIMEImage(f.read())
        img_logo.add_header("Content-ID", f"<{cid_logo}>")
        message.attach(img_logo)

    # Enviar el correo con aiosmtplib
    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True,  # Activar STARTTLS para mayor compatibilidad
        )
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")