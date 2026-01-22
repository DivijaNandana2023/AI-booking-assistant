"""
Database models for SQLite
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Customer(Base):
    """Customer table"""
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name} ({self.email})>"


class Booking(Base):
    """Booking table"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    booking_type = Column(String(255), nullable=False)
    date = Column(String(50), nullable=False)  # YYYY-MM-DD format
    time = Column(String(50), nullable=False)  # HH:MM format
    status = Column(String(50), default="confirmed")  # confirmed, cancelled, pending
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="bookings")

    def __repr__(self):
        return f"<Booking #{self.id} - {self.booking_type} on {self.date}>"

    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            "id": self.id,
            "customer_name": self.customer.name,
            "customer_email": self.customer.email,
            "customer_phone": self.customer.phone,
            "booking_type": self.booking_type,
            "date": self.date,
            "time": self.time,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "notes": self.notes,
        }
