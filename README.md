# Clone
- git clone https://github.com/your-username/your-repository.git
- cd your-repository

# Backend

## Dependencies
pip install -r backend/requirements.txt

## credentials.json

To get the credentials.json for your Google API integration (e.g., using Google Sheets API or other Google services), follow these steps:

### Step 1: Go to Google Cloud Console
- Visit the Google Cloud Console.
- If you don't already have a Google Cloud project, create a new one by clicking on the Select a project dropdown at the top and selecting New Project.

### Step 2: Enable the API
- After selecting your project, navigate to the APIs & Services section from the sidebar.
- Click Library.
- Search for the API you need, such as Google Sheets API.
- Click on the API and enable it for your project.

### Step 3: Create Service Account
- In the APIs & Services section, click on Credentials.
- Click Create credentials and select Service account.
- Provide a name for the service account and optional description, then click Create.
- Grant the service account appropriate roles, such as Editor or Owner, depending on the level of access needed. For reading and writing to Google Sheets, Editor is usually sufficient.
- Click Continue and then Done.

### Step 4: Download the Service Account Key
- After creating the service account, find it in the list of service accounts.
- Click on the email of the service account you just created.
- In the Keys section, click Add Key and select JSON.
- This will generate and download a credentials.json file that contains the necessary authentication details for the service account.

### Step 5: Store and Secure credentials.json
- Keep the credentials.json file secure and do not upload it to public repositories (e.g., GitHub).
- If you need to share the file with others, ensure it's done securely (e.g., via encrypted storage).

- Now wherever in code there is empty space . You can replace them with actual values.

- Like -:
- Path to your Google API credentials -> SERVICE_ACCOUNT_FILE = ''
- CLIENT_ID = ""
- CLIENT_SECRET = ""
- etc


# Frontend
- cd frontend
- npm install

# Database
- psql -U postgres
- CREATE DATABASE email_app;
- (Database has 2 tables email_logs and users which should be created automatically on running backen. But in the rarest case whch should not occur, use User and Email schema to create the 2 tables) 

# Start backend in a teminal in Email Folder
uvicorn backend.main:app --reload

# Start frontend in a terminal in frontend folder
npm start

# Celery worker in a terminal in a terminal
celery -A backend.celery_config.celery_app worker --loglevel=info

# Celery beat in a terminal in a terminal
celery -A backend.celery_config.celery_app worker --loglevel=info

# Ngrok to expose local backend to global in a terminal
ngrok http 8000


# Description

## Creator walkthrough
The backend is built using FastAPI, a modern Python framework for building fast and efficient APIs. It handles all the business logic, including:
- 
- User Authentication: Sign up and sign in with JWT-based token authentication.
- Email Sending via gmail and sendgrid
- Schedule emails for future delivery using Celery workers.
- Google Sheets Integration: Fetch data dynamically for email personalization. (must contain following columns only Email,Subject,Content,Time,Company_Name,Name,Template)
- Csv file upload. (must contain following columns only Email,Subject,Content,Time,Company_Name,Name,Template)
- Email Customization by Replacing placeholders ({name}, {company}) in templates.
- Database: PostgreSQL is used for storing user and email-related data.
- Once all necessary id and secrets have been added to the code, it can be deployed to use.



## User Walk Through (Any person using the app, not the one who has hosted it)
- The frontend is built with React and provides a user-friendly interface for interacting with the email-sending application. It includes:
-
- Sign Up and Sign In Pages: Users can register and log in to the application.
-
- Main Display Page:
- Displays the user’s profile and all emails sent by them. Only emails snet via sendgrid will show delivey status when webhook is triggered. Those sent via gmail will not show this as gmail does not provide this option. Send status will be available for both however.
- Allows users to select between Gmail and Sendgrid options for sending emails.
-
- Gmail:
- Leads user to an authentication page if not already authenticated where users provide access to their gmail account for sending(no other access). [In order to use this feature in testing phase, one must mention the email_id as collaborator while making google service account]
-
- SendGrid:
- If not already given the sendgrid api key to the application. It will lead to a page where user must enter their api key after getting it from sendgrid website.
- Process to Get SendGrid API Key
- Create a SendGrid Account:
- Go to SendGrid and create an account if you don’t already have one.
- Navigate to API Key Settings:
- Log in to your SendGrid dashboard.
- From the left sidebar, go to Settings > API Keys.
- Create an API Key:
- Click on Create API Key.
- Give the key a descriptive name (e.g., "Email Sending App Key").
- Assign the necessary permissions:
- If you're only sending emails, choose Restricted Access and enable Mail Send.
- Click Create & View.
- Copy the API Key immediately (you won’t be able to see it again).
- Leads users to a page where they must enter their sendgrid api key.
- Expose Your Local Webhook Endpoint:
- Install ngrok if you haven’t already:
- brew install ngrok # For macOS
- sudo apt install ngrok # For Ubuntu
- Run ngrok to expose your local FastAPI server:
- ngrok http 8000
- Go to the SendGrid dashboard.
- From the left sidebar, navigate to Settings > Mail Settings > Event Webhook.
- Enable the Event Webhook toggle.
- Paste your exposed endpoint (e.g., https://abcd1234.ngrok.io/webhook/sendgrid) into the HTTP POST URL field.
- 
- Email Customization Form:
- Custome meail by giving all necessary data - Input fields for required template data (name, company, etc.).
- File upload support for CSV files.(must contain following columns only Email,Subject,Content,Time,Company_Name,Name,Template)
- File upload support for google import sheet.(User must enable sheets api in their own google account) (must contain following columns only Email,Subject,Content,Time,Company_Name,Name,Template)
- 
- Responsive UI: Styled using modern CSS for a visually appealing and mobile-friendly interface.(Well in order to get real-time updates, user must relaod the page, as websocket could not be implemented due to time constraint)

# Contributing
If you'd like to contribute to this project, feel free to fork the repository, make changes, and create a pull request. Contributions are always welcome!

# Issues and Support
If you encounter any issues or have questions, please open an issue in the repository or reach out at kashyapbhaskar1612@gmail.com.

# Acknowledgments
This project uses:
- FastAPI for the backend.
- React for the frontend.
- PostgreSQL for the database.
- SendGrid for email delivery.
- Google for email delivery and sheets-import.
  
# Contact
For feedback or suggestions, feel free to reach out via bhaskarkashyap1612@gmail.com.
