#!/usr/bin/env python3
"""
Test direct SMTP connection și trimitere email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# SMTP Configuration
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465  # SSL
SMTP_USER = "ionut@ionesculaw.ro"
SMTP_PASSWORD = "YOUR_SMTP_PASSWORD"

def test_smtp_connection():
    """Test SMTP connection"""
    print("="*60)
    print("🔌 Testing SMTP Connection")
    print("="*60)
    print(f"Host: {SMTP_HOST}")
    print(f"Port: {SMTP_PORT}")
    print(f"User: {SMTP_USER}")
    print("="*60)

    try:
        # Connect to SMTP
        print("\n[1/3] Connecting to SMTP server...")
        smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        print("✅ Connection established")

        # Login
        print("\n[2/3] Logging in...")
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        print("✅ Login successful")

        # Create test email
        print("\n[3/3] Sending test email...")
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Ionuț Ionescu <{SMTP_USER}>"
        msg["To"] = "ionescuionut18@gmail.com"
        msg["Subject"] = "🧪 TEST DIRECT - Verificare SMTP Hostinger"

        # Plain text version
        text = """
Bună ziua,

Acesta este un email de test trimis DIRECT prin script Python pentru a verifica configurația SMTP.

Dacă primești acest email, înseamnă că SMTP-ul funcționează corect!

Timestamp: {timestamp}

Cu stimă,
Ionuț Ionescu
ionut@ionesculaw.ro
        """.format(timestamp=datetime.utcnow().isoformat())

        # HTML version
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #2563eb;">🧪 TEST DIRECT SMTP</h2>
                <p>Bună ziua,</p>
                <p>Acesta este un <strong>email de test</strong> trimis DIRECT prin script Python pentru a verifica configurația SMTP Hostinger.</p>
                <p>✅ Dacă primești acest email, înseamnă că <strong>SMTP-ul funcționează corect</strong>!</p>
                <hr>
                <p style="font-size: 12px; color: #666;">
                    Timestamp: {datetime.utcnow().isoformat()}<br>
                    Host: {SMTP_HOST}<br>
                    From: {SMTP_USER}
                </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain", "utf-8")
        part2 = MIMEText(html, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        smtp.send_message(msg)
        print("✅ Email sent successfully!")

        # Close connection
        smtp.quit()
        print("✅ Connection closed")

        print("\n" + "="*60)
        print("✅ SUCCESS - Email trimis cu succes!")
        print("="*60)
        print("\n📧 Verifică inbox-ul:")
        print("   Email: ionescuionut18@gmail.com")
        print("   Subiect: 🧪 TEST DIRECT - Verificare SMTP Hostinger")
        print("\n⏰ Așteaptă 1-2 minute și verifică:")
        print("   1. Inbox")
        print("   2. SPAM/Junk")
        print("   3. Promotions (dacă folosești Gmail)")

        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("\nPosibile cauze:")
        print("  - Parola SMTP este greșită")
        print("  - Contul de email nu există")
        print("  - Two-factor authentication activat (necesită app password)")
        return False

    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {e}")
        print("\nPosibile cauze:")
        print("  - Server SMTP indisponibil")
        print("  - Port blocat")
        print("  - Configurare greșită")
        return False

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_smtp_connection()
