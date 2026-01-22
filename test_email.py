"""
Test email configuration
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load from secrets or environment
try:
    import streamlit as st
    EMAIL_SENDER = st.secrets.get("EMAIL_SENDER")
    EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD")
except:
    import os
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)

print(f"\n📧 Email Sender: {EMAIL_SENDER}")
print(f"🔑 Password Length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0} characters")

if not EMAIL_SENDER:
    print("❌ EMAIL_SENDER not configured")
    exit(1)

if not EMAIL_PASSWORD:
    print("❌ EMAIL_PASSWORD not configured")
    exit(1)

print("\n🔄 Testing SMTP connection...")

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    print("✅ STARTTLS successful")
    
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print("✅ Authentication successful")
    
    # Test email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_SENDER  # Send to self for testing
    msg['Subject'] = "✅ Test Email from AI Booking Assistant"
    msg.attach(MIMEText("This is a test email from your AI Booking Assistant.\n\nIf you receive this, your email is configured correctly!", 'plain'))
    
    server.send_message(msg)
    print("✅ Test email sent successfully!")
    
    server.quit()
    print("\n" + "=" * 60)
    print("✅ EMAIL CONFIGURATION IS WORKING!")
    print("=" * 60)
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
    print("\n💡 SOLUTION:")
    print("   1. Make sure you enabled 2-factor authentication on Gmail")
    print("   2. Generate an App Password: https://myaccount.google.com/apppasswords")
    print("   3. Use the 16-character password in EMAIL_PASSWORD")
    exit(1)
except smtplib.SMTPException as e:
    print(f"❌ SMTP error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
