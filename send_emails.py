#!/usr/bin/env python3
"""
Script pentru trimiterea email-urilor de colaborare către service-uri auto.
Citește din data/email_queue.json și trimite email-uri folosind SMTP.
"""

import os
import json
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# SMTP Configuration (din GitHub Secrets)
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465  # SSL
SMTP_USER = os.getenv("SMTP_USER")  # ionut@ionesculaw.ro
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Email template
EMAIL_SUBJECT = "Propunere Colaborare - Recuperare Costuri Reparații Auto RCA"

EMAIL_TEMPLATE = """Bună ziua,

Vă contactez în numele firmei noastre de consultanță juridică specializată în recuperarea costurilor de reparații auto pentru autovehiculele asigurate RCA.

Înțelegem că service-ul dumneavoastră deservește zilnic clienți care au fost implicați în accidente auto cauzate de terți. În multe cazuri, acești clienți nu știu că au dreptul legal de a recupera integral costurile reparațiilor direct de la asigurătorul RCA al celui vinovat, fără a-și folosi propria asigurare CASCO.

Propunem o colaborare prin care firma noastră se ocupă de:
• Recuperarea integrală a costurilor reparațiilor de la asigurătorul RCA al vinovatului
• Gestionarea completă a dosarului (fără efort din partea service-ului sau clientului)
• Suport juridic complet pe toată durata procesului
• Comision atractiv pentru service-ul dumneavoastră la fiecare caz soluționat

Acest parteneriat vă oferă posibilitatea de a aduce un serviciu suplimentar clienților dumneavoastră, crescând satisfacția acestora și generând venituri adiționale pentru business-ul dumneavoastră.

Dacă sunteți interesat să discutăm detaliile acestei colaborări, vă rog să răspundeți la acest email sau să mă contactați telefonic.

Cu stimă,
Ionuț Ionescu
Consultant Juridic
Email: ionut@ionesculaw.ro
Website: ionesculaw.ro

---
Acest email a fost trimis automat către service-urile auto din România.
Dacă nu doriți să primiți astfel de mesaje, vă rugăm să răspundeți cu "UNSUBSCRIBE" în subiect.
"""


def create_email(recipient_email, recipient_name, service_id):
    """
    Creează un email MIME cu header-e pentru read receipt.

    Args:
        recipient_email: Adresa de email a destinatarului
        recipient_name: Numele service-ului
        service_id: ID-ul service-ului (pentru tracking)

    Returns:
        MIMEMultipart: Obiect email gata de trimis
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Ionuț Ionescu <{SMTP_USER}>"
    msg["To"] = recipient_email
    msg["Subject"] = EMAIL_SUBJECT

    # Read Receipt headers
    msg["Disposition-Notification-To"] = SMTP_USER
    msg["Return-Receipt-To"] = SMTP_USER
    msg["X-Confirm-Reading-To"] = SMTP_USER

    # Custom headers pentru tracking
    msg["X-Service-ID"] = service_id
    msg["X-Campaign"] = "auto-service-collaboration-2026"

    # Email body (text plain)
    body_text = EMAIL_TEMPLATE

    # Email body (HTML - mai frumos formatat)
    body_html = f"""
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
                    <li>✅ Recuperarea integrală a costurilor reparațiilor de la asigurătorul RCA al vinovatului</li>
                    <li>✅ Gestionarea completă a dosarului (fără efort din partea service-ului sau clientului)</li>
                    <li>✅ Suport juridic complet pe toată durata procesului</li>
                    <li>✅ Comision atractiv pentru service-ul dumneavoastră la fiecare caz soluționat</li>
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
            <p>Acest email a fost trimis automat către service-urile auto din România.<br>
            Dacă nu doriți să primiți astfel de mesaje, vă rugăm să răspundeți cu "UNSUBSCRIBE" în subiect.</p>
        </div>
    </body>
    </html>
    """

    # Attach both plain text and HTML versions
    part1 = MIMEText(body_text, "plain", "utf-8")
    part2 = MIMEText(body_html, "html", "utf-8")

    msg.attach(part1)
    msg.attach(part2)

    return msg


def send_email(smtp_conn, recipient_email, recipient_name, service_id):
    """
    Trimite un email către un destinatar.

    Args:
        smtp_conn: Conexiune SMTP activă
        recipient_email: Adresa de email
        recipient_name: Numele service-ului
        service_id: ID-ul service-ului

    Returns:
        dict: Rezultat cu status și detalii
    """
    try:
        msg = create_email(recipient_email, recipient_name, service_id)

        smtp_conn.send_message(msg)

        print(f"✅ Email sent to {recipient_name} ({recipient_email})")

        return {
            "service_id": service_id,
            "email": recipient_email,
            "name": recipient_name,
            "status": "sent",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": None
        }

    except Exception as e:
        print(f"❌ Failed to send to {recipient_name} ({recipient_email}): {e}")

        return {
            "service_id": service_id,
            "email": recipient_email,
            "name": recipient_name,
            "status": "failed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": str(e)
        }


def main():
    """
    Funcția principală - citește queue și trimite email-uri.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError(
            "SMTP credentials not set!\n"
            "Set SMTP_USER and SMTP_PASSWORD environment variables."
        )

    # Citește email queue
    queue_path = "data/email_queue.json"
    if not os.path.exists(queue_path):
        print(f"[INFO] No email queue found at {queue_path}")
        print("[INFO] Nothing to send. Exiting.")
        return

    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    recipients = queue.get("recipients", [])
    is_test = queue.get("is_test", False)

    if not recipients:
        print("[INFO] Email queue is empty. Nothing to send.")
        return

    print(f"[INFO] Found {len(recipients)} recipients in queue")
    print(f"[INFO] Test mode: {is_test}")

    # Conectare la SMTP
    print(f"[INFO] Connecting to {SMTP_HOST}:{SMTP_PORT}...")

    try:
        smtp_conn = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        smtp_conn.login(SMTP_USER, SMTP_PASSWORD)
        print("[INFO] SMTP connection established ✅")
    except Exception as e:
        print(f"[ERROR] Failed to connect to SMTP: {e}")
        return

    # Trimite email-uri
    results = []
    max_emails = 20 if not is_test else len(recipients)  # 20 per run, sau toate pentru test

    for idx, recipient in enumerate(recipients[:max_emails], 1):
        service_id = recipient.get("service_id")
        email = recipient.get("email")
        name = recipient.get("name")

        if not email:
            print(f"[WARNING] Skipping {name} - no email address")
            continue

        print(f"\n[{idx}/{min(len(recipients), max_emails)}] Sending to {name}...")

        result = send_email(smtp_conn, email, name, service_id)
        results.append(result)

        # Rate limiting - 2 secunde între email-uri
        if idx < min(len(recipients), max_emails):
            time.sleep(2)

    # Închide conexiunea SMTP
    smtp_conn.quit()
    print("\n[INFO] SMTP connection closed")

    # Salvează rezultatele
    os.makedirs("data", exist_ok=True)

    # Citește email_sent.json existent (dacă există)
    sent_path = "data/email_sent.json"
    if os.path.exists(sent_path):
        with open(sent_path, "r", encoding="utf-8") as f:
            sent_history = json.load(f)
    else:
        sent_history = {"campaigns": []}

    # Adaugă campania curentă
    campaign = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "is_test": is_test,
        "total_sent": len([r for r in results if r["status"] == "sent"]),
        "total_failed": len([r for r in results if r["status"] == "failed"]),
        "results": results
    }

    sent_history["campaigns"].append(campaign)

    # Salvează istoricul
    with open(sent_path, "w", encoding="utf-8") as f:
        json.dump(sent_history, f, indent=2, ensure_ascii=False)

    print(f"\n[INFO] Saved results to {sent_path}")

    # Golește queue-ul (sau marchează ca procesate)
    remaining = recipients[max_emails:] if len(recipients) > max_emails else []

    queue_updated = {
        "recipients": remaining,
        "is_test": False,
        "last_processed": datetime.utcnow().isoformat() + "Z"
    }

    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(queue_updated, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Updated queue - {len(remaining)} recipients remaining")

    # Statistici finale
    sent_count = len([r for r in results if r["status"] == "sent"])
    failed_count = len([r for r in results if r["status"] == "failed"])

    print(f"\n{'='*60}")
    print(f"[SUCCESS] Email campaign complete!")
    print(f"{'='*60}")
    print(f"Emails sent: {sent_count}")
    print(f"Emails failed: {failed_count}")
    print(f"Total processed: {len(results)}")
    print(f"Remaining in queue: {len(remaining)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
