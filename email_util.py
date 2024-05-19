import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def load_variables():
    return (os.getenv('MAIL_ID'), os.getenv('MAIL_PASSWORD'))

def send_email(recipient_email: str, subject: str, body: str) -> None:
    """
    Arguments: 
    recipient_email -> Email id of receiver
    subject         -> Subject of Email
    Body            -> Email Body

    Return: None
    """
    sender_email, sender_password = load_variables()
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = sender_email
    html_message['To'] = recipient_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, html_message.as_string())
        print("Mail was sent Succesfully")
    except Exception as ex:
        print(f"Error Occured while sending email: {ex}")
        return False
    finally:
        server.close()
