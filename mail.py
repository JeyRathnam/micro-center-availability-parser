import smtplib
from config import from_email, from_email_pass, to_email
from email.message import EmailMessage

def send(subject, text):
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(from_email, from_email_pass)

    message = EmailMessage()

    message.set_content(text)
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    # Send text message through SMS gateway of destination number
    server.send_message(message)