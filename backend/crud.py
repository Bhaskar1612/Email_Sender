from sqlalchemy.orm import Session
from .models import Email
from .schemas import EmailBase
from .database import User
from fastapi import HTTPException

def generate_email(prompt_template: str, row_data: dict):
    try:
        # Replace placeholders in the prompt with actual row data
        prompt = prompt_template.format(**row_data)
        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new email entry
def create_email(db: Session, email:EmailBase):
    row_data={"Name":email.name,"Company_Name":email.company_name}
    body=generate_email(email.template,row_data)
    db_email = Email(
        sender_email=email.sender,
        recipient_email=email.recipient,
        subject=email.subject   ,
        body=body,
        send_time=email.send_time,
        esp=email.esp
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

# Get all emails
def get_emails(db: Session,email_value):
    return db.query(Email).filter(Email.sender_email == email_value).all()
