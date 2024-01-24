import smtplib
import ssl
from Providors import PROVIDERS


def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "J&N Stock Analyze",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)
        print(f"SMS sent successfully to {number} via {provider}.")


def main():
    number = "6176787089"
    message = "Howdy Traders! Its me J&N Stock Analyze! Texting you from a python program!"
    provider = "Verizon"

    sender_credentials = ("jnstockanalyize@gmail.com", "tplr znil sobq eazj")

    try:
        send_sms_via_email(number, message, provider, sender_credentials)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
