from fastapi import FastAPI, BackgroundTasks, Form
import aiosmtplib
from email.mime.text import MIMEText
from app.core.config import settings
from pathlib import Path
import certifi
import ssl
from app.core.security import security_manager
from fastapi import HTTPException, status
import asyncio


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
        """Send email with proper timeout and error handling.
        
        This method handles errors gracefully and does not raise exceptions,
        making it safe for use in background tasks. Errors are logged instead.
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password]):
            error_msg = "SMTP configuration is incomplete. Please check your environment variables."
            print(f"❌ {error_msg}")
            return False
        
        message = MIMEText(body, "html")
        message["From"] = self.smtp_user
        message["To"] = to_email
        message["Subject"] = subject
        
        print(
            f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port} as {self.smtp_user} to send to {to_email}"
        )

        smtp = None
        try:
            smtp = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                tls_context=ssl.create_default_context(cafile=certifi.where()),
                timeout=30,  # 30 second timeout for connection
            )

            # ✅ Await all async calls with timeout
            await asyncio.wait_for(smtp.connect(), timeout=30.0)
            await asyncio.wait_for(smtp.login(self.smtp_user, self.smtp_password), timeout=30.0)
            await asyncio.wait_for(smtp.send_message(message), timeout=30.0)
            await asyncio.wait_for(smtp.quit(), timeout=10.0)
            print(f"✅ Email sent successfully to {to_email}")
            return True
        except asyncio.TimeoutError as e:
            error_msg = f"SMTP connection timeout while sending email to {to_email}: {str(e)}"
            print(f"❌ {error_msg}")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            # Don't raise exception - log and return False for background task safety
            return False
        except Exception as e:
            error_msg = f"Failed to send email to {to_email}: {str(e)}"
            print(f"❌ {error_msg}")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            # Don't raise exception - log and return False for background task safety
            return False

    # Note: verify_email method should be in a separate service or router
    # This method has dependencies that don't belong in EmailService
