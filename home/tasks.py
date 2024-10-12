from celery import shared_task
from django.core.mail import send_mail
import os
from django.core.mail import BadHeaderError

@shared_task
def enviar_correo(asunto, mensaje, destinatarios):
    try:
        send_mail(
            asunto,
            mensaje,
            os.environ.get('EMAIL_HOST_USER'),
            destinatarios, 
            fail_silently=False,
        )
    except BadHeaderError:
        print("Error en la cabecera del correo.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

#IMPORTANTE

#mi entendimiento de celery a cerca a nulo y por ende no se porque al ejecutar celery normalmente el sistema de correos no sirve

#celery -A core worker --pool=solo -l info


#esta linea (especificamente --pool=solo) basicamente convierte los procesos a single thread,y magicamente funciona todo cool.

#yo no pregunto, solo estoy agradecido.