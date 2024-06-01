from PIL import Image
from pathlib import Path
from pydantic import EmailStr
import smtplib

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_image(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_big = image.resize((1000, 500))
    image_resized_small = image.resize((200, 100))
    image_resized_big.save(f"app/static/images/resized_big_{image_path.name}")
    image_resized_small.save(f"app/static/images/resized_small_{image_path.name}")


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to = email_to
    message_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(message_content)
