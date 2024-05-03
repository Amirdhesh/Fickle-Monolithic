import logging  # noqa: F401
from celery import Celery
from app.core.settings import settings
from app.utils import send_email_for_email_verification, send_email_for_forget_password

celery_app = Celery("send_email_task", broker=settings.CELERY_BROKER,backend=settings.CELERY_BACKEND)


celery_app.task(name="Sending email for verification")


def send_otp_for_email_verification(receiver_email: str, otp: str):
    send_email_for_email_verification(receiver_email, otp)


celery_app.task(name="Sending email for forget password")


def send_otp_for_forget_password(receiver_email: str, otp: str):
    send_email_for_forget_password(receiver_email, otp)
