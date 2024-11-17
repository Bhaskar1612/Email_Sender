from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from .auth_utils import get_db
from .database import User


import base64

def send_email_via_gmail(sender_email, recipient_email, subject, content, access_token, refresh_token):
    # Create the credentials object from access and refresh tokens
    credentials = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='774611051832-q446pib18hdj68r80lp6rmcd77cerb36.apps.googleusercontent.com',
        client_secret='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'
    )

    # Refresh the credentials if they have expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        
        db=get_db()
        # If the credentials were refreshed, update the tokens in the database
        new_access_token = credentials.token
        new_refresh_token = credentials.refresh_token if credentials.refresh_token else refresh_token

        # Update the access and refresh tokens in the database
        user = db.query(User).filter(User.email == sender_email).first()
        if user:
            user.access_token = new_access_token
            user.refresh_token = new_refresh_token
            db.commit()
            print(f"Tokens updated for {sender_email}")
        else:
            print(f"User with email {sender_email} not found.")

    # Now, you can use the credentials to authenticate and send the email
    service = build('gmail', 'v1', credentials=credentials)

    # Define the email message structure
    message = create_message(sender_email, recipient_email, subject, content)

    # Send the email
    send_message(service, "me", message)

    db=next(get_db())
    user = db.query(User).filter(User.email == sender_email).first()
    user.delivery_satus='Not Applicable'
    db.commit()

    print(f"Email sent from {sender_email} to {recipient_email}")

# Function to create the email message
def create_message(sender, to, subject, body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    return {'raw': raw_message}

# Function to send the email message via Gmail API
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Sent message to {message["to"]} Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')