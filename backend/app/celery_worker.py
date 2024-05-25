import logging  # noqa: F401
from celery import Celery
from app.core.settings import settings
from app.utils import send_email_for_email_verification, send_email_for_forget_password

celery_app = Celery("task", broker=settings.CELERY_BROKER,backend=settings.CELERY_BACKEND)
logger = logging.getLogger(__name__)

@celery_app.task(name="Sending email for verification")
def send_email_verification(receiver_email: str, token: str):
        try:
                send_email_for_email_verification(receiver_email=receiver_email,token=token)
        except Exception as e:
                logger.exception(f"Failed to send OTP {e}")
        


@celery_app.task(name="Sending email for forget password")
def send_otp_for_forget_password(receiver_email: str, otp: str):
        try:
                send_email_for_forget_password(receiver_email=receiver_email,otp=otp)
        except Exception as e:
                logger.exception(f"Failed to send OTP {e}")
    
