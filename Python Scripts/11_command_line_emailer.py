from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def draft_email(pSender,pReceivier):
    # --- Create Message ---
    message = MIMEMultipart()
    message["From"] = pSender
    message["To"] = pReceivier
    print("Input Subject line")
    message["Subject"] = input()
    print("Add email body")
    body = input()
    message.attach(MIMEText(body, "plain"))

    return message

def send_email(pSender,pSenderPwd,pReceivier,pMessage):
    # --- Send Email ---
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() # Secure the connection
        server.login(pSender, pSenderPwd)
        server.sendmail(pSender, pReceivier, pMessage.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

load_dotenv()
vSender = os.getenv("user_email")
vSenderPwd = os.getenv("user_passkey")
vReceiver = os.getenv("receiver_email")

vMessage = draft_email(vSender,vReceiver)

send_email(vSender,vSenderPwd,vReceiver,vMessage)

