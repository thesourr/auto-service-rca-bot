#!/usr/bin/env python3
"""
Generează lista de email-uri pentru BCC în Apple Mail
"""

import json
import csv

def generate_bcc_list():
    """Generate BCC list from services CSV"""

    print("="*70)
    print("📧 GENERATOR LISTĂ BCC - Apple Mail")
    print("="*70)

    # Read services from CSV
    services_with_email = []

    with open("data/services.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("email"):
                services_with_email.append({
                    "name": row["name"],
                    "email": row["email"],
                    "city": row["city"]
                })

    print(f"\n✅ Found {len(services_with_email)} services with email")

    # Generate BCC string (comma-separated)
    bcc_emails = [s["email"] for s in services_with_email]
    bcc_string = ", ".join(bcc_emails)

    # Save to file
    with open("email_bcc_list.txt", "w", encoding="utf-8") as f:
        f.write(bcc_string)

    print(f"✅ Saved BCC list to: email_bcc_list.txt")
    print(f"📊 Total emails: {len(bcc_emails)}")

    # Save detailed list
    with open("email_detailed_list.txt", "w", encoding="utf-8") as f:
        f.write("LISTA COMPLETĂ EMAIL-URI\n")
        f.write("="*70 + "\n\n")
        for idx, service in enumerate(services_with_email, 1):
            f.write(f"{idx}. {service['name']} ({service['city']})\n")
            f.write(f"   Email: {service['email']}\n\n")

    print(f"✅ Saved detailed list to: email_detailed_list.txt")

    # Instructions
    print("\n" + "="*70)
    print("📝 CUM SĂ FOLOSEȘTI ÎN APPLE MAIL")
    print("="*70)
    print("\n1. Deschide Apple Mail")
    print("\n2. Click 'New Message' (Cmd+N)")
    print("\n3. Completează:")
    print("   - To: ionut@ionesculaw.ro (email-ul tău - pentru test)")
    print("   - Subject: Propunere Colaborare - Recuperare Costuri Reparații Auto RCA")
    print("\n4. Click 'BCC' (dacă nu vezi, apasă Cmd+Shift+B)")
    print("\n5. Copiază conținutul din 'email_bcc_list.txt' și lipește în BCC")
    print("\n6. Scrie mesajul (vezi template mai jos)")
    print("\n7. Click 'Send'")
    print("\n" + "="*70)
    print("📧 EMAIL TEMPLATE")
    print("="*70)
    print("""
Bună ziua,

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
    """)

    print("="*70)
    print("⚠️  IMPORTANTE:")
    print("="*70)
    print("\n1. Apple Mail poate avea LIMITE:")
    print(f"   - Gmail: max 500 destinatari/email")
    print(f"   - Tu ai: {len(bcc_emails)} email-uri")
    print(f"   - Dacă > 500, trebuie să trimiți în batch-uri")

    if len(bcc_emails) > 500:
        print(f"\n⚠️  ATENȚIE: Ai {len(bcc_emails)} email-uri!")
        print("   Trebuie să trimiți în multiple batch-uri de max 500")
        print("   Voi genera batch-uri automat...")

        # Generate batches
        batch_size = 500
        batches = [bcc_emails[i:i+batch_size] for i in range(0, len(bcc_emails), batch_size)]

        for idx, batch in enumerate(batches, 1):
            batch_string = ", ".join(batch)
            filename = f"email_bcc_batch_{idx}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(batch_string)
            print(f"   ✅ Batch {idx}: {len(batch)} emails → {filename}")

    print("\n2. TEST ÎNAINTE:")
    print("   - Trimite DOAR către tine în BCC pentru test")
    print("   - Verifică că email-ul arată bine")
    print("   - Apoi trimite către toți")

    print("\n3. RATE LIMITING:")
    print("   - Nu trimite mai mult de 500 email-uri/zi")
    print("   - Așteaptă 24h între batch-uri")
    print("   - Evită să fii marcat ca spam")

    print("\n" + "="*70)

if __name__ == "__main__":
    generate_bcc_list()
