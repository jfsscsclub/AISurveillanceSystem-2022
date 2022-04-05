from email.message import EmailMessage
import smtplib
from getpass import getpass

mail_server = smtplib.SMTP_SSL('smtp.gmail.com')

sender_email = "csclub.surveillancesystem.demo@gmail.com"
sender_pw = getpass()

mail_server.login(sender_email, sender_pw)

def notifyUserWithAttachment(user_email, formatted_timestamp):
    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = user_email

    message["Subject"] = f"Person Detected at {formatted_timestamp}"
    message.set_content(f"""
    A person was detected at {formatted_timestamp}. A picture has been attached to this email.
    """)

    with open(f"{formatted_timestamp}.jpg", 'rb') as file:
        message.add_attachment(
            file.read(),
            maintype="image",
            subtype="jpeg",
            filename=f"{formatted_timestamp}.jpg"
        )

    mail_server.send_message(message)
