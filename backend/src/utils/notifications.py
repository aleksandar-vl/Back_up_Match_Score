from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from src.core.config import settings


def send_email_notification(email: str, subject: str, message: str) -> None:
    """
    Sends an email notification with the specified
    subject and message to the given email address.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email message.

    Raises:
        Exception: If there is an error sending the email.
    """

    try:
        sender_email = settings.EMAIL_SENDER
        password = settings.EMAIL_PASSWORD

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject

        color = "#007bff"
        if subject == "Request Accepted":
            color = "#28a745"
        elif subject == "Request Rejected":
            color = "#dc3545"

        html_message = f"""
        <html>
          <body style="font-family: Arial, sans-serif; 
          max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #f8f9fa; border-radius: 
            10px; padding: 20px; text-align: center;">
              <h1 style="color: {color}; margin-bottom: 20px;">{subject} 🐾</h1>

              <div style="background-color: 
              white; border-radius: 8px; padding: 20px; 
              margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="font-size: 16px; color: #333; line-height: 1.5;">
                  {message}
                </p>
              </div>

              <div style="margin-top: 20px; padding: 15px; 
              background-color: #e9ecef; border-radius: 8px;">
                <p style="color: #6c757d; font-size: 14px; margin: 0;">
                  This is an automated notification from 
                  Kittens Strike Match Score website
                </p>
              </div>
            </div>
          </body>
        </html>
        """

        msg.attach(MIMEText(html_message, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

    except Exception as e:
        print(f"Error sending email: {e}")
