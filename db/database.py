import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from db.models import Base, Customer, Booking
from app.config import DATABASE_PATH
from datetime import datetime
from typing import Optional, List


class DatabaseManager:
    """Handles all database operations"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()

    # ===================== CUSTOMER =====================

    def add_or_get_customer(self, name: str, email: str, phone: str) -> Customer:
        """Add or get customer by email"""
        session = self.get_session()
        try:
            customer = session.query(Customer).filter(Customer.email == email).first()
            if not customer:
                customer = Customer(name=name, email=email, phone=phone)
                session.add(customer)
                session.commit()
                session.refresh(customer)
            return customer
        finally:
            session.close()

    # ===================== BOOKING =====================

    def create_booking(
        self,
        customer_id: int,
        booking_type: str,
        date: str,
        time: str,
        notes: str = None,
    ) -> Booking:
        """Create a new booking"""
        session = self.get_session()
        try:
            booking = Booking(
                customer_id=customer_id,
                booking_type=booking_type,
                date=date,
                time=time,
                notes=notes,
                status="confirmed",
            )
            session.add(booking)
            session.commit()
            session.refresh(booking)
            return booking
        finally:
            session.close()

    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Get booking by ID (with customer eagerly loaded)"""
        session = self.get_session()
        try:
            booking = (
                session.query(Booking)
                .options(joinedload(Booking.customer))
                .filter(Booking.id == booking_id)
                .first()
            )
            return booking
        finally:
            session.close()

    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings (with customer eagerly loaded)"""
        session = self.get_session()
        try:
            bookings = (
                session.query(Booking)
                .options(joinedload(Booking.customer))
                .all()
            )
            return bookings
        finally:
            session.close()

    def get_bookings_by_email(self, email: str) -> List[Booking]:
        """Get bookings for a specific email"""
        session = self.get_session()
        try:
            bookings = (
                session.query(Booking)
                .options(joinedload(Booking.customer))
                .join(Customer)
                .filter(Customer.email == email)
                .all()
            )
            return bookings
        finally:
            session.close()

    def get_bookings_by_date(self, date: str) -> List[Booking]:
        """Get bookings for a specific date"""
        session = self.get_session()
        try:
            bookings = (
                session.query(Booking)
                .options(joinedload(Booking.customer))
                .filter(Booking.date == date)
                .all()
            )
            return bookings
        finally:
            session.close()

    def update_booking_status(self, booking_id: int, status: str) -> bool:
        """Update booking status"""
        session = self.get_session()
        try:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if booking:
                booking.status = status
                session.commit()
                return True
            return False
        finally:
            session.close()

    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking"""
        session = self.get_session()
        try:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if booking:
                session.delete(booking)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def get_booking_count(self) -> int:
        """Get total number of bookings"""
        session = self.get_session()
        try:
            count = session.query(Booking).count()
            return count
        finally:
            session.close()

    # ===================== UTIL =====================

    def get_formatted_datetime(self) -> str:
        """Get formatted current datetime"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ===================== EMAIL =====================

    def send_email(self, to_email: str, subject: str, body: str) -> tuple:
        """Send email notification for booking
        Returns: (success: bool, message: str)
        """
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from app.config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

        try:
            if not EMAIL_SENDER or EMAIL_SENDER == "your-email@gmail.com":
                return False, "Email sender not configured"

            if not EMAIL_PASSWORD or EMAIL_PASSWORD == "your-16-char-app-password":
                return False, "Email password not configured"

            msg = MIMEMultipart()
            msg["From"] = EMAIL_SENDER
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            return True, "Email sent successfully"

        except smtplib.SMTPAuthenticationError:
            return False, "Email authentication failed. Check your password."
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Error sending email: {str(e)}"
