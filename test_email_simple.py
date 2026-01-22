import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os

sys.path.insert(0, '.')

EMAIL_SENDER = "divijanandanadavire@gmail.com"
EMAIL_PASSWORD = "vhxxoddokgvohxje"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

print("EMAIL CONFIGURATION TEST")
print("-" * 50)
print(f"Email: {EMAIL_SENDER}")
print(f"Password Length: {len(EMAIL_PASSWORD)}")
print("-" * 50)

try:
    print("\nConnecting to SMTP server...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    print("Connected!")
    
    print("Starting TLS...")
    server.starttls()
    print("TLS started!")
    
    print("Logging in...")
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print("Login successful!")
    
    print("\nSending test email...")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_SENDER
    msg['Subject'] = "Test Email - AI Booking Assistant"
    msg.attach(MIMEText("Test email from booking assistant!", 'plain'))
    
    server.send_message(msg)
    print("Email sent!")
    
    server.quit()
    print("\nSUCCESS: Email is working!")
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {str(e)}")
