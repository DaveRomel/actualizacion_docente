import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path
from schema.inscripcion_schema import NotificacionInscripcionSchema
load_dotenv()

async def send_email(subject, data: NotificacionInscripcionSchema,email):
    # Obtener variables del .env y corregir el tipo de datos
    smtp_host = os.getenv("SMTP_HOST_FA")
    smtp_port = int(os.getenv("SMTP_EMAIL_PORT_FA"))  # Convertir puerto a int
    smtp_user = os.getenv("SMTP_EMAIL_USERNAME_FA")
    smtp_password = os.getenv("SMTP_EMAIL_PASSWORD_FA")

    # Cargar el archivo HTML como plantilla
    with open(Path(__file__).parent / "email_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Reemplazar las variables en el HTML
    html_body = html_template.format(**data.dict())  # Reemplazar la variable nombre en el HTML

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = email  
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html", "utf-8"))


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