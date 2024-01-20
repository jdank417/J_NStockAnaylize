import smtplib
import os  # Add this line
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from google_auth_oauthlib.flow import InstalledAppFlow  # Add this line
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def send_email(subject, body, to_email):
    # Set up the SMTP server for Gmail with SSL
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'jnstockanalyize@gmail.com'  # Replace with your Gmail address
    token_path = 'token.json'  # Path to store the OAuth token

    # Create the email message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Load or create OAuth token
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # If there are no valid credentials available, let the user log in.
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Connect to the SMTP server using SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Authenticate with OAuth token
            server.ehlo()
            server.login(smtp_username, 'user_oauth2_token')

            # Send the email
            server.sendmail(smtp_username, to_email, message.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    email_subject = "Hello from your Python program!"
    email_body = "This is the body of the email. You can customize it as needed."
    recipient_email = "nicoabonanno@gmail.com"  # Replace with the recipient's email address

    send_email(email_subject, email_body, recipient_email)
