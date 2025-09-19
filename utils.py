import pandas as pd
import smtplib
from email.mime.text import MIMEText

def export_to_excel(data, filename="survey_results.xlsx"):
    df = pd.DataFrame([data])
    df.to_excel(filename, index=False)
    return filename

def send_email(subject, body, to_emails):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@dmv-training-app.com"
    msg['To'] = ", ".join(to_emails)

    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
    except Exception as e:
        print("Email send failed:", e)
