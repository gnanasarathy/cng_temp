import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

def load_variables():
    return (os.getenv('MAIL_ID'), os.getenv('MAIL_PASSWORD'))

def send_email(recipient_email: str, subject: str, body: str, file_path: str = None) -> None:
    """
    Arguments: 
    recipient_email -> Email id of receiver
    subject         -> Subject of Email
    Body            -> Email Body
    file_path       -> Path to the file to be attached

    Return: None
    """
    sender_email, sender_password = load_variables()
    
    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach body
    message.attach(MIMEText(body, 'plain'))
    if file_path is not None:
        # Attach file
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')

        message.attach(part)

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Mail was sent successfully")
    except Exception as ex:
        print(f"Error occurred while sending email: {ex}")


