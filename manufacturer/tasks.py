import random
import smtplib
from django.core.serializers import json, deserialize
from celery import shared_task
from .models import Network
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from manufacturer.generate_qr import generate_qr_code


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
        # Получите объект сети
        network = Network.objects.get(pk=network_id)

        # Сгенерируйте QR-код
        qr_code_data = generate_qr_code(network)

        # Отправьте QR-код на адрес электронной почты пользователя
        subject = "QR Code for Network Contact Info"
        message = "Here is the QR code with contact information for the network."
        from_email = "your_email@gmail.com"  # Ваша почта
        recipient_list = [user_email]

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = user_email

        text = MIMEText(message)
        msg.attach(text)

        image = MIMEImage(qr_code_data, name="qr_code.png")
        msg.attach(image)

        # Отправка письма
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=msg.as_string())

    except Network.DoesNotExist:
        print("Network not found.")
    except Exception as e:
        print("Error:", str(e))
