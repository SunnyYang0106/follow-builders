import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

BUILDERS = [
    "Sam Altman", "Greg Brockman", "Andrej Karp​​​​​​​​​​​​​​​​

