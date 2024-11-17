from celery import Celery
from .gmail import send_email_via_gmail  
from .auth_utils import get_db  
from .database import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from . import models
from datetime import datetime
from .sendgrid import send_email_via_sendgrid

import pytz

# Get the current UTC time as a timezone-aware datetime object
now_utc = datetime.now(pytz.UTC)

# Create Celery app
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def send_pending_emails():
    db_gen = get_db()
    db = next(db_gen)
    # Query for the first email log with send_status as 'pending'
    pending_email = db.query(models.Email).filter(models.Email.send_status.in_(['pending', 'failed']),models.Email.send_time <= now_utc).order_by(models.Email.send_time).first()

    if not pending_email:
        raise HTTPException(status_code=404, detail="No pending emails found")

    sender_email = pending_email.sender_email
    recipient_email = pending_email.recipient_email
    subject = pending_email.subject
    content = pending_email.body
    esp = pending_email.esp 

    # Send email using Gmail API
    try:
        user = db.query(User).filter(User.email == sender_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if esp == "gmail":
            # Retrieve the user's access and refresh token based on the sender email
            
            # Call Gmail sending function
            send_email_via_gmail(
                sender_email, recipient_email, subject, content,
                user.access_token, user.refresh_token
            )
        elif esp == "sendgrid":
            # Call SendGrid sending function, using Reply-To as sender email
            send_email_via_sendgrid(
                sender_email=sender_email,  # Reply-To set to user's email
                recipient_email=recipient_email,
                subject=subject,
                content=content
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported ESP")

        # After sending email, update the send_status to 'sent'
        pending_email.send_status = 'sent'
        db.commit()  # Save the changes

        return {"status": "Email sent successfully"}

    except Exception as e:
        # If email sending fails, update the send_status to 'failed'
        pending_email.send_status = 'failed'
        db.commit()

        raise HTTPException(status_code=500, detail=f"An error occurred while sending email: {str(e)}")