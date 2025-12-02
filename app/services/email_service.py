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
        
        # Debug: Print SMTP configuration (mask password)
        print("=" * 80)
        print("📧 SMTP Configuration Check:")
        print(f"  SMTP_HOST: {self.smtp_host}")
        print(f"  SMTP_PORT: {self.smtp_port} (type: {type(self.smtp_port)})")
        print(f"  SMTP_USER: {self.smtp_user}")
        print(f"  SMTP_PASSWORD: {'*' * len(self.smtp_password) if self.smtp_password else 'None'}")
        print(f"  All configured: {all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password])}")
        print("=" * 80)

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
            # Create SSL context - Gmail requires proper SSL/TLS
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            print(f"🔌 Creating SMTP connection to {self.smtp_host}:{self.smtp_port}")
            smtp = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                tls_context=ssl_context,
                timeout=30,  # 30 second timeout for connection
            )

            # ✅ Await all async calls with timeout
            print("📡 Step 1: Connecting to SMTP server...")
            await asyncio.wait_for(smtp.connect(), timeout=30.0)
            print("✅ Connected successfully")
            
            print("🔐 Step 2: Logging in...")
            await asyncio.wait_for(smtp.login(self.smtp_user, self.smtp_password), timeout=30.0)
            print("✅ Login successful")
            
            print("📨 Step 3: Sending message...")
            await asyncio.wait_for(smtp.send_message(message), timeout=30.0)
            print("✅ Message sent")
            
            print("👋 Step 4: Closing connection...")
            await asyncio.wait_for(smtp.quit(), timeout=10.0)
            print(f"✅ Email sent successfully to {to_email}")
            return True
        except asyncio.TimeoutError as e:
            error_msg = f"SMTP connection timeout while sending email to {to_email}: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            # Don't raise exception - log and return False for background task safety
            return False
        except aiosmtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP authentication failed for {to_email}. Check your SMTP_USER and SMTP_PASSWORD. Error: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"   Note: Gmail requires an 'App Password' if 2FA is enabled, not your regular password.")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            return False
        except aiosmtplib.SMTPException as e:
            error_msg = f"SMTP error while sending email to {to_email}: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            return False
        except Exception as e:
            error_msg = f"Failed to send email to {to_email}: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            if smtp:
                try:
                    await smtp.quit()
                except:
                    pass
            # Don't raise exception - log and return False for background task safety
            return False

    # Note: verify_email method should be in a separate service or router
    # This method has dependencies that don't belong in EmailService
