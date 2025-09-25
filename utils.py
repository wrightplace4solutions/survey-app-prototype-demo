import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from typing import Dict, List, Any

def export_to_excel(
    data: Dict[str, Any],
    filename: str = "survey_results.xlsx",
    sheet_name: str = "responses",
) -> str:
    """Append a single submission (dict) to an Excel file.

    This implementation avoids direct openpyxl workbook access ("writer.book") to
    keep type checkers happy and remains robust:
    - If the file/sheet exists, it reads existing rows and concatenates a new row.
    - Otherwise, it creates a new file/sheet with headers.
    """
    new_df = pd.DataFrame([data])

    if os.path.exists(filename):
        try:
            existing = pd.read_excel(  # type: ignore[reportUnknownMemberType]
                filename, sheet_name=sheet_name, engine="openpyxl"
            )
            out_df = pd.concat([existing, new_df], ignore_index=True)
        except ValueError:
            # Sheet doesn't exist yet – just use the new row
            out_df = new_df
    else:
        out_df = new_df

    # Always overwrite with the combined frame – simpler and reliable
    out_df.to_excel(  # type: ignore[reportUnknownMemberType]
        filename,
        sheet_name=sheet_name,
        index=False,
        engine="openpyxl",
    )

    return filename

def send_email(subject: str, body: str, to_emails: List[str]) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@training-survey-app.com"
    msg["To"] = ", ".join(to_emails)

    try:
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
    except (smtplib.SMTPException, ConnectionError, OSError) as e:
        print("Email send failed:", e)
