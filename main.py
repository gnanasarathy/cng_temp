from email_util import send_email
recipient_email = "sarathy.alagesan309@gmail.com"
subject = "Test Subject"
body = """
<html>
  <body>
    <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
  </body>
</html>
"""

send_email(recipient_email, subject, body)

