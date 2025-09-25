"""Utility helpers for exporting survey data and sending emails.

This module provides two small utilities used by the Streamlit app:
- export_to_excel: append a single response dict to an Excel worksheet
- send_email: send a simple plaintext email via a local SMTP relay

Notes
-----
- Import order follows Pylint's convention: stdlib first, then third‑party.
- All functions are side‑effect free except for file/network IO.
"""

from typing import Any, Dict, List
import os
import smtplib
from email.mime.text import MIMEText

import pandas as pd

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
    """Send a simple plaintext email using a local SMTP relay.

    Parameters
    ----------
    subject: str
        The email subject line.
    body: str
        The email body content as plain text.
    to_emails: List[str]
        One or more recipient email addresses.

    This function attempts to use an SMTP server available at localhost.
    Failures are printed to stdout rather than raising to avoid breaking
    the Streamlit app during demos.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@training-survey-app.com"
    msg["To"] = ", ".join(to_emails)

    try:
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
    except (smtplib.SMTPException, ConnectionError, OSError) as e:
        print("Email send failed:", e)