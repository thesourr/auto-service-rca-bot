#!/usr/bin/env python3
"""
Script LOCAL pentru trimitere email-uri
Rulează pe computerul tău când vrei să trimiți campanie
"""

import os
import json
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# SMTP Configuration
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = "ionut@ionesculaw.ro"
SMTP_PASSWORD = "YOUR_SMTP_PASSWORD"

# Email template
EMAIL_SUBJECT = "Propunere Colaborare - Recuperare Costuri Reparații Auto RCA"

EMAIL_TEMPLATE_TEXT = """Bună ziua,

Sunt Ionuț Ionescu, consultant juridic specializat în recuperarea daunelor RCA.

Vă scriu pentru a vă propune o colaborare care poate aduce beneficii atât service-ului dumneavoastră, cât și clienților acestuia.

Multe dintre persoanele implicate în accidente rutiere nu cunosc faptul că pot recupera integral costurile reparațiilor direct de la asigurătorul RCA al părții vinovate, fără a utiliza CASCO-ul propriu.

Serviciile noastre includ:

- Recuperarea costurilor reparațiilor de la asiguratorul RCA
- Gestionarea completă a documentației și procedurilor legale
- Consultanță juridică pe toată durata procesului
- Comision pentru service la fiecare dosar soluționat cu succes

Această colaborare permite service-ului dumneavoastră să ofere un serviciu complementar clienților, îmbunătățind experiența acestora și generând venituri suplimentare.

Dacă această propunere v-ar putea interesa, vă rog să îmi răspundeți la acest email pentru a discuta detaliile.

Cu stimă,
Ionuț Ionescu
Consultant Juridic
Email: ionut@ionesculaw.ro
Tel: [număr telefon]

Dacă preferați să nu mai primiți mesaje de acest tip, vă rog să răspundeți cu "STOP" în subiect.
"""

EMAIL_TEMPLATE_HTML = """
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .benefits {{
            background-color: white;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }}
        .benefits ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .benefits li {{
            margin: 8px 0;
        }}
        .signature {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
        }}
        .footer {{
            font-size: 12px;
            color: #777;
            text-align: center;
            padding: 15px;
            background-color: #f0f0f0;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Propunere Colaborare</h2>
        <p>Recuperare Costuri Reparații Auto RCA</p>
    </div>

    <div class="content">
        <p>Bună ziua,</p>

        <p>Vă contactez în numele firmei noastre de consultanță juridică specializată în <strong>recuperarea costurilor de reparații auto</strong> pentru autovehiculele asigurate RCA.</p>

        <p>Înțelegem că service-ul dumneavoastră deservește zilnic clienți care au fost implicați în accidente auto cauzate de terți. În multe cazuri, acești clienți nu știu că au dreptul legal de a recupera integral costurile reparațiilor direct de la asigurătorul RCA al celui vinovat, fără a-și folosi propria asigurare CASCO.</p>

        <div class="benefits">
            <h3>Propunem o colaborare prin care firma noastră se ocupă de:</h3>
            <ul>
                <li>Recuperarea integrală a costurilor reparațiilor de la asigurătorul RCA al vinovatului</li>
                <li>Gestionarea completă a dosarului (fără efort din partea service-ului sau clientului)</li>
                <li>Suport juridic complet pe toată durata procesului</li>
                <li>Comision atractiv pentru service-ul dumneavoastră la fiecare caz soluționat</li>
            </ul>
        </div>

        <p>Acest parteneriat vă oferă posibilitatea de a aduce un serviciu suplimentar clienților dumneavoastră, crescând satisfacția acestora și generând venituri adiționale pentru business-ul dumneavoastră.</p>

        <p>Dacă sunteți interesat să discutăm detaliile acestei colaborări, vă rog să răspundeți la acest email sau să mă contactați telefonic.</p>

        <div class="signature">
            <p><strong>Cu stimă,</strong><br>
            <strong>Ionuț Ionescu</strong><br>
            Consultant Juridic<br>
            Email: <a href="mailto:ionut@ionesculaw.ro">ionut@ionesculaw.ro</a><br>
            Website: <a href="https://ionesculaw.ro">ionesculaw.ro</a></p>
        </div>
    </div>

    <div class="footer">
        <p>Dacă preferați să nu mai primiți mesaje de acest tip, vă rog să răspundeți cu "STOP" în subiect.</p>
    </div>
</body>
</html>
"""

def send_email(smtp_conn, recipient_email, recipient_name, service_id):
    """Send email to recipient"""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Ionuț Ionescu <{SMTP_USER}>"
        msg["To"] = recipient_email
        msg["Subject"] = EMAIL_SUBJECT
        msg["Reply-To"] = SMTP_USER

        # Read receipts
        msg["Disposition-Notification-To"] = SMTP_USER
        msg["Return-Receipt-To"] = SMTP_USER
        msg["X-Confirm-Reading-To"] = SMTP_USER

        # Custom headers
        msg["X-Service-ID"] = service_id
        msg["X-Campaign"] = "auto-service-collaboration-2026"

        # Attach text and HTML
        part1 = MIMEText(EMAIL_TEMPLATE_TEXT, "plain", "utf-8")
        part2 = MIMEText(EMAIL_TEMPLATE_HTML, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)

        smtp_conn.send_message(msg)

        print(f"  ✅ Email sent to {recipient_name} ({recipient_email})")

        return {
            "email": recipient_email,
            "name": recipient_name,
            "status": "sent",
            "timestamp": datetime.now().isoformat(),
            "error": None
        }

    except Exception as e:
        print(f"  ❌ Failed to send to {recipient_name} ({recipient_email}): {e}")

        return {
            "email": recipient_email,
            "name": recipient_name,
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def main():
    """Main function"""
    print("="*70)
    print("📧 LOCAL EMAIL SENDER - Service Auto RCA")
    print("="*70)

    # Check for recipients file
    if not os.path.exists("email_recipients.json"):
        print("\n❌ ERROR: Fișierul 'email_recipients.json' nu există!")
        print("\nPași:")
        print("1. Deschide dashboard-ul: https://thesourr.github.io/auto-service-rca-bot/")
        print("2. Selectează service-urile dorite")
        print("3. Click 'Download Email List' (sau exportă lista)")
        print("4. Salvează fișierul ca 'email_recipients.json' în acest folder")
        print("5. Rulează din nou acest script")
        return

    # Load recipients
    with open("email_recipients.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    recipients = data.get("recipients", [])

    if not recipients:
        print("\n⚠️  WARNING: Lista de recipienți este goală!")
        return

    print(f"\n📊 Found {len(recipients)} recipients")
    print(f"🔐 SMTP: {SMTP_HOST}:{SMTP_PORT}")
    print(f"📤 From: {SMTP_USER}")
    print("\n" + "="*70)

    # Confirm
    response = input(f"\n❓ Trimite email-uri către {len(recipients)} service-uri? (yes/no): ")
    if response.lower() not in ['yes', 'y', 'da']:
        print("❌ Anulat.")
        return

    print("\n🚀 Starting email campaign...\n")

    # Connect to SMTP
    try:
        print(f"[1/3] Connecting to {SMTP_HOST}...")
        smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        print("  ✅ Connected")

        print(f"[2/3] Logging in as {SMTP_USER}...")
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        print("  ✅ Logged in")

        print(f"[3/3] Sending {len(recipients)} emails...\n")

        results = []

        for idx, recipient in enumerate(recipients, 1):
            service_id = recipient.get("service_id", "unknown")
            email = recipient.get("email")
            name = recipient.get("name", "Unknown Service")

            if not email:
                print(f"  ⚠️  Skipping {name} - no email")
                continue

            print(f"[{idx}/{len(recipients)}] Sending to {name}...")

            result = send_email(smtp, email, name, service_id)
            results.append(result)

            # Delay between emails (2 seconds)
            if idx < len(recipients):
                time.sleep(2)

        smtp.quit()
        print("\n  ✅ SMTP connection closed")

        # Save results
        results_file = f"email_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump({
                "campaign_date": datetime.now().isoformat(),
                "total_sent": len([r for r in results if r["status"] == "sent"]),
                "total_failed": len([r for r in results if r["status"] == "failed"]),
                "results": results
            }, f, indent=2, ensure_ascii=False)

        # Summary
        sent_count = len([r for r in results if r["status"] == "sent"])
        failed_count = len([r for r in results if r["status"] == "failed"])

        print("\n" + "="*70)
        print("✅ EMAIL CAMPAIGN COMPLETE!")
        print("="*70)
        print(f"📨 Emails sent: {sent_count}")
        print(f"❌ Emails failed: {failed_count}")
        print(f"📁 Results saved: {results_file}")
        print("="*70)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
