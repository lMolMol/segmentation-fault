import re
from email.message import EmailMessage
import ssl ## Extra layer of security
import smtplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv

from Syllabot.back.src.Ai.Ai import byWeek
from Syllabot.data.CourseSyllabus import CourseSyllabus

# Use the environment variables
EMAIL_SENDER ="syllabot2025@gmail.com"
EMAIL_PASSWORD = "mshe ltqj bqil taoe"



def send_html_email(email_receiver, subject, body):
    email = EmailMessage()
    email['From'] = EMAIL_SENDER
    email['To'] = email_receiver
    email['Subject'] = subject
    email.add_alternative(body, subtype='html')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(email)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

## Example
email_receiver = "mahamedyossef51@gmail.com"
subject = "Weekly update from Syllabot"

def format_email_body(ai_response):
    # Convert markdown-like syntax to HTML
    ai_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', ai_response)  # Bold text
    ai_response = re.sub(r'\* (.*?)\n', r'<li>\1</li>', ai_response)  # List items
    ai_response = re.sub(r'\n\n', r'</ul><br><ul>', ai_response)  # Separate sections with spacing
    ai_response = f"<ul>{ai_response}</ul>"

    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h2 {{
                color: #2c3e50;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .date {{
                font-weight: bold;
                color: #2980b9;
            }}
            .important {{
                font-weight: bold;
                color: #e74c3c;
            }}
            br {{
                margin-bottom: 15px;
                display: block;
            }}
        </style>
    </head>
    <body>
        {ai_response}
    </body>
    </html>
    """
    return body

def sendEmail(week, Syllabus, email):
    ai_response = byWeek(week, Syllabus)
    formatted_body = format_email_body(ai_response)
    msg = MIMEText(formatted_body, 'html')
    print(msg)
    send_html_email(email, subject, msg)

#sendEmail("2", CourseSyllabus.SYLLABUS, e)