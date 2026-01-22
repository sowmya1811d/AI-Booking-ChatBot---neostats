import smtplib
from email.message import EmailMessage

def send_email(sender, password, receiver, body):
    msg = EmailMessage()

    # This controls how the sender name appears
    msg["From"] = "DocAI Assistant <{}>".format(sender)
    msg["To"] = receiver
    msg["Subject"] = "Appointment Confirmation – DocAI"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
