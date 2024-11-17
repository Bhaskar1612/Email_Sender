
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from fastapi import HTTPException
from .auth_utils import get_db
from .database import User



def send_email_via_sendgrid(sender_email: str, recipient_email: str, subject: str, content: str):
    try:
        db=next(get_db())
        SENDGRID_API_KEY=db.query(User).filter(User.email == sender_email).first().sendgrid_api_key
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        # Use your default email as the sender
        mail = Mail(
            from_email=Email(sender_email),
            to_emails=To(recipient_email),
            subject=subject,
            plain_text_content=Content("text/plain", content)
        )
        # Set the reply-to address to the user's email
        mail.reply_to = Email(sender_email)
        response = sg.send(mail)

        if response.status_code not in range(200, 300):
            raise HTTPException(status_code=500, detail="Failed to send email via SendGrid")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SendGrid error: {str(e)}")
