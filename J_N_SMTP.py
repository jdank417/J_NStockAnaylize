import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, app_password, recipient_email, subject, message):
    print("Setting up the MIME...")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    print("Connecting to the SMTP server...")
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()

        print("Logging in to Gmail account...")
        server.login(sender_email, app_password)

        print("Sending the email...")
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print("Email sent successfully!")

def main():

    sender_email = 'jnstockanalyize@gmail.com'
    app_password = 'tplr znil sobq eazj'
    recipient_email = 'jasondank@yahoo.com'
    subject = 'J&N Stock Analyze'
    message = "Howdy Traders! Its me J&N Stock Analyze! Emailing you from a python program!"


    send_email(sender_email, app_password, recipient_email, subject, message)

if __name__ == "__main__":
    main()
