#!/usr/bin/env python3
"""
Test SMTP cu logging detaliat și verificare email
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# SMTP Configuration
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = "ionut@ionesculaw.ro"
SMTP_PASSWORD = "YOUR_SMTP_PASSWORD"

def test_detailed_smtp():
    """Test SMTP with detailed logging"""
    print("="*70)
    print("🔍 DETAILED SMTP TEST")
    print("="*70)

    # Test 1: Trimite la ionescuionut18@gmail.com
    print("\n📧 Test 1: Gmail (ionescuionut18@gmail.com)")
    send_test_email("ionescuionut18@gmail.com", "Gmail Test")

    # Test 2: Trimite înapoi la ionut@ionesculaw.ro (self-test)
    print("\n📧 Test 2: Self-test (ionut@ionesculaw.ro)")
    send_test_email("ionut@ionesculaw.ro", "Self Test")

    # Test 3: Încearcă și un Yahoo email (dacă ai)
    # send_test_email("your_email@yahoo.com", "Yahoo Test")

def send_test_email(recipient, test_name):
    """Send test email with detailed logging"""
    try:
        logging.info(f"Starting {test_name} to {recipient}")

        # Connect
        logging.info(f"Connecting to {SMTP_HOST}:{SMTP_PORT}")
        smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        smtp.set_debuglevel(1)  # Enable SMTP debug output

        logging.info("Connected successfully")

        # Login
        logging.info(f"Logging in as {SMTP_USER}")
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        logging.info("Login successful")

        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Ionut Ionescu <{SMTP_USER}>"
        msg["To"] = recipient
        msg["Subject"] = f"🧪 {test_name} - {datetime.now().strftime('%H:%M:%S')}"
        msg["Message-ID"] = f"<test-{datetime.now().timestamp()}@ionesculaw.ro>"
        msg["Reply-To"] = SMTP_USER

        # Simple text
        text = f"""
TEST EMAIL - {test_name}

Acesta este un email de test trimis la {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

Recipient: {recipient}
From: {SMTP_USER}
Host: {SMTP_HOST}

Dacă primești acest email, te rog confirmă!

---
Ionut Ionescu
ionut@ionesculaw.ro
        """

        html = f"""
        <html>
            <body style="font-family: Arial; padding: 20px;">
                <h2 style="color: #2563eb;">🧪 TEST EMAIL - {test_name}</h2>
                <p>Acesta este un email de test trimis la <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong>.</p>
                <hr>
                <p><strong>Recipient:</strong> {recipient}<br>
                <strong>From:</strong> {SMTP_USER}<br>
                <strong>Host:</strong> {SMTP_HOST}</p>
                <hr>
                <p style="color: green; font-weight: bold;">✅ Dacă primești acest email, te rog confirmă!</p>
                <p>---<br>Ionut Ionescu<br>ionut@ionesculaw.ro</p>
            </body>
        </html>
        """

        msg.attach(MIMEText(text, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))

        # Send
        logging.info(f"Sending email to {recipient}")
        result = smtp.send_message(msg)
        logging.info(f"Send result: {result}")

        smtp.quit()
        logging.info("Connection closed")

        print(f"✅ {test_name} - Email sent successfully to {recipient}")
        print(f"   Check inbox în 1-2 minute!")

    except Exception as e:
        logging.error(f"❌ {test_name} failed: {e}", exc_info=True)
        print(f"❌ {test_name} - FAILED: {e}")

if __name__ == "__main__":
    test_detailed_smtp()

    print("\n" + "="*70)
    print("📋 SUMMARY")
    print("="*70)
    print("\n✅ Verifică următoarele inbox-uri în 1-2 minute:")
    print("   1. ionescuionut18@gmail.com")
    print("      - Inbox")
    print("      - Spam/Junk")
    print("      - Promotions")
    print("      - All Mail")
    print("\n   2. ionut@ionesculaw.ro (self-test)")
    print("      - Login în Hostinger Webmail")
    print("      - Verifică Inbox")
    print("\n⚠️  IMPORTANT:")
    print("   - Dacă primești self-test DAR NU Gmail → Gmail blochează")
    print("   - Dacă nu primești NIMIC → Problemă cu Hostinger sending")
    print("="*70)
