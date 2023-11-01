import random
import smtplib
import qrcode
from django.core.serializers import deserialize
from celery import shared_task
from .models import Network
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from io import BytesIO


@shared_task
def clear_debt_async(serialized_objects):
    objects = list(deserialize("json", serialized_objects))
    for obj in objects:
        network = obj.object
        network.debt = 0
        network.save()


@shared_task
def edit_debt():
    networks = Network.objects.all()
    for network in networks:
        random_debt_increase = random.randint(5, 500)
        network.debt += random_debt_increase
        network.save()


@shared_task
def decrease_debt():
    networks = Network.objects.all()
    for network in networks:
        random_debt = random.randint(100, 10000)
        network.debt = max(0, network.debt - random_debt)
        network.save()


@shared_task
def generate_qr_code_and_send_email(network_id, user_email):
    try:
        network = Network.objects.get(pk=network_id)

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(network.name)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        img_byte_array.seek(0)

        from_email = settings.EMAIL_HOST_USER
        to_email = user_email

        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        msg = MIMEMultipart()

        message = "Here is the QR code with contact information for the network."
        msg.attach(MIMEText(message, "plain"))

        image = MIMEImage(img_byte_array.read(), name="qr_code.png", content_type="image/png")
        msg.attach(image)

        msg["Subject"] = "QR Code for Network Contact Info"
        msg["From"] = from_email
        msg["To"] = to_email

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

    except Network.DoesNotExist:
        print("Network not found.")
    except Exception as e:
        print("Error:", str(e))
