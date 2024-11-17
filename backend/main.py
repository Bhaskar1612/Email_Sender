from fastapi import FastAPI, Depends, UploadFile, HTTPException, File, Request,APIRouter,Form
from sqlalchemy.orm import Session
from . import models, crud 
import pandas as pd
from . import sheets_service
from .schemas import EmailBase
from .database import User
from .auth_utils import hash_password, verify_password, create_jwt_token,get_db,get_current_user,UserLogin,Token,UserCreate
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlencode
import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
 # Ensure correct import of the celery instance


app = FastAPI()

router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this to your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Login Endpoint
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_jwt_token(data={"sub": db_user.email})
    return {"username":db_user.username,"access_token": access_token, "token_type": "bearer","email":db_user.email}

@app.get("/protected-route")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}!"}

CLIENT_ID = "774611051832-q446pib18hdj68r80lp6rmcd77cerb36.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/oauth2callback"
SCOPE = "https://www.googleapis.com/auth/gmail.send"
api_key = "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"


@app.get("/check_gmail")
async def check_gmail(email: str = Query(..., description="Enter your Gmail address"),
                     db: Session = Depends(get_db)):
    existing_user = (
    db.query(User)
    .filter(User.email == email)
    .filter(User.access_token.isnot(None), User.access_token != "")
    .first()
    )
    if not existing_user:
        return False
    return True

@app.get("/check_sendgrid")
async def check_sendgrid(email: str = Query(..., description="Enter your Email address"),
                     db: Session = Depends(get_db)):
    existing_user = (
    db.query(User)
    .filter(User.email == email)
    .filter(User.sendgrid_api_key != "")
    .first()
    )
    if not existing_user:
        return False
    return True

@app.post("/add_sendgrid")
async def add_sendgrid(email: str ,sendgrid_api_key:str,
                     db: Session = Depends(get_db)):
    existing_user = (
    db.query(User)
    .filter(User.email == email).first()
    )
    existing_user.sendgrid_api_key=sendgrid_api_key
    db.commit()

@app.get("/email_stats")
def get_email_status_count(email: str, db: Session = Depends(get_db)):
    """
    Endpoint to get the count of emails by status for the given email address.
    """
    # Validate input email
    if not email:
        raise HTTPException(status_code=400, detail="Email parameter is required.")
    
    # Query the database for each status
    total_count = db.query(models.Email).filter(models.Email.sender_email == email).count()
    pending_count = db.query(models.Email).filter(
        models.Email.sender_email == email, models.Email.send_status == "pending"
    ).count()
    failed_count = db.query(models.Email).filter(
        models.Email.sender_email == email, models.Email.send_status == "failed"
    ).count()
    sent_count = db.query(models.Email).filter(
        models.Email.sender_email == email, models.Email.send_status == "sent"
    ).count()

    # Return counts
    return {
        "email": email,
        "total_count": total_count,
        "pending_count": pending_count,
        "failed_count": failed_count,
        "sent_count": sent_count,
    }

    

# Step 1: Start OAuth2 Flow
@app.get("/start-auth")
async def start_auth(email: str = Query(..., description="Enter your Gmail address"),
                     db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Construct Google authorization URL
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode({
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "state": email
        })
    )
    
    return RedirectResponse(auth_url)

# Step 2: OAuth2 Callback - Exchange code for tokens
@app.get("/oauth2callback")
async def oauth2callback(code: str, state:str,db: Session = Depends(get_db)):
    # Use the email from the session or passed as part of the query (depends on your app logic)
    # Retrieve the email from the database based on the OAuth callback
    # Ideally, you should store email in the session or pass it via the query string (same as start-auth)
    email=state
    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    # Request access and refresh tokens from Google
    response = requests.post(token_url, data=data)
    tokens = response.json()
    
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    # Find the user in the database using email (you might want to store email in session or query)
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Update user's access token and refresh token
        user.access_token = access_token
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}



async def generate_email(prompt_template: str, row_data: dict):
    try:
        # Replace placeholders in the prompt with actual row data
        prompt = prompt_template.format(**row_data)
        return {"generated_content": prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a new email entry to the database
@app.post("/add_email/")
def add_email(email: EmailBase, db: Session = Depends(get_db)):
    return crud.create_email(db=db, email=email)

# Get list of emails from the database
@app.get("/emails/")
def get_emails(email: str, db: Session = Depends(get_db)):
    return crud.get_emails(db,email)


@app.post("/upload_csv/")
async def upload_csv(sender:str= Form(...), esp:str= Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    # Read CSV data into a DataFrame
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    
    # Process each row in the CSV and add to the database
    for _, row in df.iterrows():
        email_data = EmailBase(
            sender=sender,
            recipient=row['Email'],
            subject=row['Subject'],
            send_time=row['Time'],
            esp=esp,
            name=row['Name'],
            company_name=row['Company_Name'],
            template=row['Template']
        )
        crud.create_email(db, email=email_data)
    
    return {"message": "CSV uploaded and emails added to the database"}


@app.post("/import_google_sheet/")
def import_google_sheet(sender:str= Form(...),esp:str= Form(...),spreadsheet_id: str= Form(...), range_name: str= Form(...), db: Session = Depends(get_db)):
    try:
        # Read data from Google Sheets
        df = sheets_service.read_google_sheet(spreadsheet_id, range_name)
        if df.empty:
            raise HTTPException(status_code=400, detail="No data found in the specified sheet range")
        
        # Process each row and add to the database
        for _, row in df.iterrows():
            email_data = EmailBase(
                sender=sender,
                recipient=row['Email'],
                subject=row['Subject'],
                send_time=row['Time'],
                esp=esp,
                name=row['Name'],
                company_name=row['Company_Name'],
                template=row['Template']
            )
            crud.create_email(db, email=email_data)

        return {"message": "Data imported from Google Sheets and emails added to the database"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import logging
logging.basicConfig(level=logging.INFO)

@app.post("/sendgrid-webhook")
async def sendgrid_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        # Parse incoming JSON data from SendGrid
        events = await request.json()
        logging.info(f"Received webhook data: {events}")
        
        for event in events:
            # Extract event data
            email = event.get("email")
            event_type = event.get("event")  # e.g., delivered, open, bounce, etc.
            timestamp = event.get("timestamp")

            # Fetch the email log entry matching the recipient email
            email_log = db.query(models.Email).filter(models.Email.recipient_email == email, models.Email.send_status == 'sent',models.Email.esp!='gmail').first()

            # Update the status based on the event type from SendGrid
            if email_log:
                # Map SendGrid event type to your application's delivery_status field
                if event_type == "delivered":
                    email_log.delivery_status = "delivered"
                elif event_type == "open":
                    email_log.delivery_status = "opened"
                elif event_type == "bounce":
                    email_log.delivery_status = "bounced"
                elif event_type == "dropped":
                    email_log.delivery_status = "failed"

                # Save updates
                db.commit()
        
        return {"status": "Events processed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")






