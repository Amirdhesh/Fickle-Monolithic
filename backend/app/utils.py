import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from app.core.settings import settings


emailverification_templete = Path("app/email-templete/emailverification_templete.html")
forgetpassword_templete = Path("app/email-templete/forgetpassword_templete.html")


def send_email_for_email_verification(receiver_email : str, otp : str):
    sender_email : str = settings.SENDER_EMAIL
    sender_password : str = settings.SENDER_EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your OTP for email verification"
    
    with emailverification_templete.open(mode='r',encoding='utf-8') as file:
        templete = file.read()
    email_body = templete.replace("{{otp}}",str(otp))
    msg.attach(MIMEText(email_body,"html"))
    

    with smtplib.SMTP(host = "smtp.gmail.com",port=587) as server:
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,receiver_email,msg.as_string())



def send_email_for_forget_password(receiver_email : str, otp : str):
    sender_email : str = settings.SENDER_EMAIL
    sender_password : str = settings.SENDER_EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your OTP for email verification"
    
    with forgetpassword_templete.open(mode='r',encoding='utf-8') as file:
        templete = file.read()
    email_body = templete.replace("{{otp}}",str(otp))
    msg.attach(MIMEText(email_body,"html"))
    

    with smtplib.SMTP(host = "smtp.gmail.com",port=587) as server:
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,receiver_email,msg.as_string())