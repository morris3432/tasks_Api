import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config.config import Config

config = Config()


def send_email(recipient_email: str, password: str):
  sender_email = config.correo  # Tu dirección de correo electrónico
  sender_password = config.clave

  # Crear el mensaje
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = recipient_email
  message["Subject"] = "Contraseña"

  # Cuerpo del mensaje
  body = f"Tu nuevo password es: {password}, gracias por unirte a la app"
  message.attach(MIMEText(body, "plain"))

  try:
    # Conectar al servidor SMTP de Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, sender_password)
      text = message.as_string()  # Convierte el mensaje a formato de texto
      server.sendmail(sender_email, recipient_email, text)  # Envía el correo

      print("Correo enviado exitosamente.")
  except Exception as e:
    print(f"Error al enviar correo: {e}")
