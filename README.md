# Clone
git clone https://github.com/your-username/your-repository.git
cd your-repository

# Backend

## Dependencies
pip install -r backend/requirements.txt

## credentials.json

To get the credentials.json for your Google API integration (e.g., using Google Sheets API or other Google services), follow these steps:

### Step 1: Go to Google Cloud Console
Visit the Google Cloud Console.
If you don't already have a Google Cloud project, create a new one by clicking on the Select a project dropdown at the top and selecting New Project.

### Step 2: Enable the API
After selecting your project, navigate to the APIs & Services section from the sidebar.
Click Library.
Search for the API you need, such as Google Sheets API.
Click on the API and enable it for your project.

### Step 3: Create Service Account
In the APIs & Services section, click on Credentials.
Click Create credentials and select Service account.
Provide a name for the service account and optional description, then click Create.
Grant the service account appropriate roles, such as Editor or Owner, depending on the level of access needed. For reading and writing to Google Sheets, Editor is usually sufficient.
Click Continue and then Done.

### Step 4: Download the Service Account Key
After creating the service account, find it in the list of service accounts.
Click on the email of the service account you just created.
In the Keys section, click Add Key and select JSON.
This will generate and download a credentials.json file that contains the necessary authentication details for the service account.

### Step 5: Store and Secure credentials.json
Keep the credentials.json file secure and do not upload it to public repositories (e.g., GitHub).
If you need to share the file with others, ensure it's done securely (e.g., via encrypted storage).

Now wherever in code there is empty space . You can replace them with actual values.

Like -:
Path to your Google API credentials -> SERVICE_ACCOUNT_FILE = ''
CLIENT_ID = ""
CLIENT_SECRET = ""
etc


# Frontend
cd frontend
npm install

# Database
psql -U postgres
CREATE DATABASE email_app;
(Database has 2 tables email_logs and users which should be created automatically on running backen. But in the rarest case whch should not occur, use User and Email schema to create the 2 tables) 

# Start backend in a teminal
uvicorn main:app --reload

# Start frontend in a terminal
npm start

# Celery worker in a terminal
celery -A backend.celery_config.celery_app worker --loglevel=info

# Celery beat in a terminal
celery -A backend.celery_config.celery_app worker --loglevel=info

# Ngrok to expose local backend to global ina terminal
ngrok http 8000

