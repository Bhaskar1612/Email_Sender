from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Email(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    sender_email = Column(String(255), nullable=False)         # Sender's email address
    recipient_email = Column(String(255), nullable=False)      # Recipient's email address
    subject = Column(String(255), nullable=False)              # Email subject
    body = Column(Text, nullable=False)                        # Email content (body)
    send_status = Column(String(50), default="pending")        # Send status (default: "pending")
    send_time = Column(DateTime, default=datetime.utcnow)      # Timestamp of when the email was scheduled or sent
    delivery_status = Column(String(50), nullable=True)        # Delivery status (optional, updated after sending)
    error_message = Column(Text, nullable=True)                # Error message in case of failure (optional)
    esp = Column(String, nullable=False, default="gmail")