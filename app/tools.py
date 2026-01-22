"""
Tool implementations for RAG, Booking, Email, and optional Web Search
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Tuple
from datetime import datetime

from app.config import (
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    SENDGRID_API_KEY,
)
from db.database import DatabaseManager


# ===================== RAG TOOL =====================

class RAGTool:
    """Tool for RAG-based document retrieval and answering"""

    def __init__(self, rag_pipeline):
        self.rag_pipeline = rag_pipeline

    def retrieve_and_answer(self, query: str) -> str:
        """Answer using full RAG pipeline"""
        try:
            return self.rag_pipeline.ask(query)
        except Exception as e:
            return f"RAG error: {str(e)}"

    def get_status(self) -> str:
        count = self.rag_pipeline.get_document_count()
        if count == 0:
            return "No documents loaded"
        return f"{count} documents loaded and indexed"


# ===================== BOOKING TOOL =====================

class BookingPersistenceTool:
    """Tool for saving bookings to database"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_booking(self, booking_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        try:
            required_fields = ["name", "email", "phone", "booking_type", "date", "time"]
            if not all(field in booking_data for field in required_fields):
                return False, {"error": "Missing required fields"}

            if not self._validate_email(booking_data["email"]):
                return False, {"error": "Invalid email format"}

            if not self._validate_date(booking_data["date"]):
                return False, {"error": "Invalid date format (use YYYY-MM-DD)"}

            if not self._validate_time(booking_data["time"]):
                return False, {"error": "Invalid time format (use HH:MM)"}

            customer = self.db.add_or_get_customer(
                booking_data["name"],
                booking_data["email"],
                booking_data["phone"],
            )

            booking = self.db.create_booking(
                customer.id,
                booking_data["booking_type"],
                booking_data["date"],
                booking_data["time"],
                booking_data.get("notes", ""),
            )

            return True, {
                "booking_id": booking.id,
                "customer_id": customer.id,
                "message": f"Booking #{booking.id} confirmed!",
                "customer_email": customer.email,
            }

        except Exception as e:
            return False, {"error": f"Database error: {str(e)}"}

    def _validate_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validate_date(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _validate_time(self, time_str: str) -> bool:
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False


# ===================== EMAIL TOOL =====================

class EmailTool:
    """Tool for sending email confirmations"""

    def __init__(self):
        self.sender = EMAIL_SENDER
        self.password = EMAIL_PASSWORD

    def send_confirmation_email(
        self,
        to_email: str,
        booking_id: int,
        customer_name: str,
        booking_type: str,
        date: str,
        time: str,
    ) -> Tuple[bool, str]:

        try:
            subject = f"Booking Confirmation - #{booking_id}"
            body = self._generate_email_body(
                customer_name, booking_id, booking_type, date, time
            )

            if self.sender and self.password:
                return self._send_via_smtp(to_email, subject, body)
            else:
                return False, "Email credentials not configured"

        except Exception as e:
            return False, f"Email send failed: {str(e)}"

    def _send_via_smtp(self, to_email: str, subject: str, body: str) -> Tuple[bool, str]:
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            return True, "Email sent successfully"
        except Exception as e:
            return False, f"SMTP error: {str(e)}"

    def _generate_email_body(
        self, name: str, booking_id: int, booking_type: str, date: str, time: str
    ) -> str:
        return f"""
        <html>
            <body>
                <h2>Booking Confirmation</h2>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Your booking is confirmed.</p>
                <p><b>Booking ID:</b> {booking_id}</p>
                <p><b>Service:</b> {booking_type}</p>
                <p><b>Date:</b> {date}</p>
                <p><b>Time:</b> {time}</p>
                <p>Thank you!</p>
            </body>
        </html>
        """


# ===================== TOOL EXECUTOR =====================

class ToolExecutor:
    def __init__(self, rag_pipeline, db_manager: DatabaseManager):
        self.rag_tool = RAGTool(rag_pipeline)
        self.booking_tool = BookingPersistenceTool(db_manager)
        self.email_tool = EmailTool()

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        if tool_name == "rag_retrieval":
            result = self.rag_tool.retrieve_and_answer(kwargs.get("query", ""))
            return {"success": True, "result": result}

        elif tool_name == "save_booking":
            success, result = self.booking_tool.save_booking(kwargs.get("booking_data", {}))
            return {"success": success, "result": result}

        elif tool_name == "send_email":
            success, message = self.email_tool.send_confirmation_email(
                to_email=kwargs.get("to_email"),
                booking_id=kwargs.get("booking_id"),
                customer_name=kwargs.get("customer_name"),
                booking_type=kwargs.get("booking_type"),
                date=kwargs.get("date"),
                time=kwargs.get("time"),
            )
            return {"success": success, "message": message}

        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}
