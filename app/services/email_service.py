from fastapi import FastAPI, BackgroundTasks, Form
import aiosmtplib
from email.mime.text import MIMEText
from app.core.config import settings
from pathlib import Path
import certifi
import ssl
from app.core.security import security_manager
from fastapi import HTTPException, status


class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.BASE_DIR = Path(__file__).resolve().parent.parent

    def get_template(self, template_name: str):
        template_path = self.BASE_DIR / "utils" / "templates" / f"{template_name}.html"
        with open(template_path, "r") as file:
            return file.read()

    async def send_email(self, to_email: str, subject: str, body: str):
        message = MIMEText(body, "html")
        message["From"] = self.smtp_user
        message["To"] = to_email
        message["Subject"] = subject

        print(
            f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port} as {self.smtp_user}"
        )

        smtp = aiosmtplib.SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            start_tls=True,
            tls_context=ssl.create_default_context(cafile=certifi.where()),
        )

        # ✅ Await all async calls
        await smtp.connect()
        await smtp.login(self.smtp_user, self.smtp_password)
        await smtp.send_message(message)
        await smtp.quit()

    # Note: verify_email method should be in a separate service or router
    # This method has dependencies that don't belong in EmailService
