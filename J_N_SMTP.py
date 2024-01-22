import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, app_password, recipient_email, subject, message):
    print("Setting up the MIME...")
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the MIME
    msg.attach(MIMEText(message, 'plain'))

    print("Connecting to the SMTP server...")
    # Connect to the SMTP server (Gmail server in this case)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start TLS for security
        server.starttls()

        print("Logging in to Gmail account...")
        # Log in to your Gmail account using App Password
        server.login(sender_email, app_password)

        print("Sending the email...")
        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print("Email sent successfully!")

def main():
    # Replace these with your Gmail credentials and recipient email
    sender_email = 'jnstockanalyize@gmail.com'
    app_password = 'tplr znil sobq eazj'
    recipient_email = 'jasondank@yahoo.com'
    subject = 'J&N Stock Analyze'
    message = "Howdy Traders! Its me J&N Stock Analyze! Emailing you from a python program!"

    # Call the function to send the email
    send_email(sender_email, app_password, recipient_email, subject, message)

if __name__ == "__main__":
    main()
