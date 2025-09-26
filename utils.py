"""Utility helpers for exporting survey data and sending emails."""

from typing import Any, Dict, List
import os
import smtplib
from email.mime.text import MIMEText

import pandas as pd

# Optional: try to read Streamlit secrets if available
def _get_secret(name: str, default: str | None = None) -> str | None:
    try:
        import streamlit as st  # type: ignore
        if "secrets" in dir(st) and name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)

def export_to_excel(
    data: Dict[str, Any],
    filename: str = "survey_results.xlsx",
    sheet_name: str = "responses",
) -> str:
    """Append a single submission (dict) to an Excel file."""
    new_df = pd.DataFrame([data])

    if os.path.exists(filename):
        try:
            existing = pd.read_excel(filename, sheet_name=sheet_name, engine="openpyxl")  # type: ignore
            out_df = pd.concat([existing, new_df], ignore_index=True)
        except ValueError:
            out_df = new_df
    else:
        out_df = new_df

    out_df.to_excel(filename, sheet_name=sheet_name, index=False, engine="openpyxl")  # type: ignore
    return filename


def send_email(subject: str, body: str, to_emails: List[str]) -> None:
    """Send plain-text email using SendGrid API when available; otherwise try localhost SMTP."""
    # 1) Try SendGrid (recommended)
    sg_key = _get_secret("sendgrid_api_key")
    from_email = _get_secret("from_email", "noreply@soulwaresystems.com")

    if sg_key:
        try:
            from sendgrid import SendGridAPIClient  # type: ignore
            from sendgrid.helpers.mail import Mail  # type: ignore

            for recipient in to_emails:
                message = Mail(
                    from_email=from_email,
                    to_emails=recipient,
                    subject=subject,
                    plain_text_content=body,
                )
                SendGridAPIClient(sg_key).send(message)
            return
        except Exception as e:  # noqa: BLE001
            print("SendGrid send failed, falling back to SMTP:", e)

    # 2) Fallback: local SMTP relay (optional; okay if it fails silently)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    try:
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
    except Exception as e:  # noqa: BLE001
        print("SMTP send failed:", e)
