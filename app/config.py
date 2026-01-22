"""
Configuration module for the AI Booking Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Try to get from Streamlit secrets first, then env variables
try:
    import streamlit as st
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    EMAIL_SENDER = st.secrets.get("EMAIL_SENDER", os.getenv("EMAIL_SENDER", "your-email@gmail.com"))
    EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", os.getenv("EMAIL_PASSWORD", ""))
except:
    # Fallback if not in Streamlit context
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

OPENAI_MODEL = "gpt-4-turbo-preview"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "booking_assistant.db")

# RAG Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 5

# Booking Configuration
REQUIRED_BOOKING_FIELDS = ["name", "email", "phone", "booking_type", "date", "time"]
MEMORY_LENGTH = 25  # Number of messages to keep in memory

# Application Configuration
APP_NAME = "AI Booking Assistant"
MAX_PDF_SIZE_MB = 25

# Dummy Email API for testing (SendGrid would replace this)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# Service Types (customize based on your booking domain)
SERVICE_TYPES = [
    "Salon/Haircut",
    "Medical Consultation",
    "Hotel Booking",
    "Event Reservation",
    "Class/Training",
    "Other"
]
