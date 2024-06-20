import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from app.core.settings import settings


def load_email_template(*, template_path: Path):
    try:
        with template_path.open(mode="r", encoding="utf-8") as file:
            template = file.read()
        return template
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found {template_path}")
    except Exception as e:
        raise Exception(e)


def send_mail(*, sender_email: str, receiver_email: str, msg: str):
    try:
        sender_password: str = settings.SENDER_EMAIL_PASSWORD
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg)
    except Exception as e:
        raise Exception(f"Unable to send mail: {e}")


def send_email_for_email_verification(*, receiver_email: str, token: str):
    sender_email: str = settings.SENDER_EMAIL
    email_verification_template_path = Path(
        r"D:\Projects\Fickel\Monolithic\backend\app\template\emailverification_template.html"
    )
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Link for email verification"

    template = load_email_template(template_path=email_verification_template_path)
    URL = f"http://localhost:8000/v1.0.0/user/verify-email/?token={token}&email={receiver_email}"

    email_body = template.replace("{{URL}}", str(URL))
    msg.attach(MIMEText(email_body, "html"))
    ("HELLO")
    send_mail(
        sender_email=sender_email, receiver_email=receiver_email, msg=msg.as_string()
    )


def send_email_for_forget_password(*, receiver_email: str, otp: str):
    sender_email: str = settings.SENDER_EMAIL
    forget_password_template_path = Path("app/template/forget_password_template.html")
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your OTP for password reset"

    template = load_email_template(template_path=forget_password_template_path)
    email_body = template.replace("{{ otp }}", str(otp))
    msg.attach(MIMEText(email_body, "html"))

    send_mail(
        sender_email=sender_email, receiver_email=receiver_email, msg=msg.as_string()
    )
