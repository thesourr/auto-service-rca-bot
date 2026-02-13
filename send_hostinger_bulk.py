#!/usr/bin/env python3
"""
Bulk email sender for Hostinger SMTP using recipients JSON.

Security model:
- SMTP credentials are read from environment variables only.
- No secrets are stored in code or output files.
"""

import argparse
import json
import os
import re
import smtplib
import ssl
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


DEFAULT_INPUT = "/Users/ionut/Downloads/email_recipients.json"
DEFAULT_SUBJECT = "Propunere Colaborare - Recuperare Costuri Reparatii Auto RCA"
DEFAULT_DELAY_SECONDS = 2.0

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


DEFAULT_TEXT_TEMPLATE = """Buna ziua,

Sunt Ionut Ionescu, consultant juridic specializat in recuperarea daunelor RCA.

Va scriu pentru a va propune o colaborare care poate aduce beneficii atat service-ului dumneavoastra, cat si clientilor acestuia.

Multe persoane implicate in accidente rutiere nu stiu ca pot recupera integral costurile reparatiilor direct de la asiguratorul RCA al partii vinovate, fara a utiliza CASCO-ul propriu.

Serviciile noastre includ:
- Recuperarea costurilor reparatiilor de la asiguratorul RCA
- Gestionarea completa a documentatiei si procedurilor legale
- Consultanta juridica pe toata durata procesului
- Comision pentru service la fiecare dosar solutionat cu succes

Daca aceasta propunere va poate interesa, raspundeti la acest email pentru detalii.

Cu stima,
Ionut Ionescu
Consultant Juridic
Email: ionut@ionesculaw.ro
"""


DEFAULT_HTML_TEMPLATE = """<html>
<body style="font-family:Arial,sans-serif;line-height:1.6;color:#222">
  <p>Buna ziua,</p>
  <p>Sunt <b>Ionut Ionescu</b>, consultant juridic specializat in recuperarea daunelor RCA.</p>
  <p>Va propun o colaborare prin care oferim:</p>
  <ul>
    <li>Recuperarea costurilor reparatiilor de la asiguratorul RCA</li>
    <li>Gestionarea completa a documentatiei si procedurilor legale</li>
    <li>Consultanta juridica pe toata durata procesului</li>
    <li>Comision pentru service la fiecare dosar solutionat cu succes</li>
  </ul>
  <p>Daca va intereseaza, raspundeti la acest email pentru detalii.</p>
  <p>Cu stima,<br>Ionut Ionescu<br>Consultant Juridic<br>ionut@ionesculaw.ro</p>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send bulk email through Hostinger SMTP.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to recipients JSON file.")
    parser.add_argument("--subject", default=DEFAULT_SUBJECT, help="Email subject.")
    parser.add_argument("--from-name", default="Ionut Ionescu", help="Display name in From header.")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS, help="Delay between emails (seconds).")
    parser.add_argument("--limit", type=int, default=0, help="Max recipients to send (0 = all).")
    parser.add_argument("--dry-run", action="store_true", help="Validate list and print plan without sending.")
    parser.add_argument("--text-template", default="", help="Optional text template file path.")
    parser.add_argument("--html-template", default="", help="Optional HTML template file path.")
    parser.add_argument("--resume-file", default="data/email_sent.json", help="JSON file with already sent addresses.")
    parser.add_argument("--results-dir", default="data", help="Directory for per-run result JSON.")
    return parser.parse_args()


def normalize_email(raw: str) -> str:
    if not raw:
        return ""
    cleaned = raw.strip().strip(";").strip(",").strip().rstrip(".").lower()
    return cleaned


def is_valid_email(email_value: str) -> bool:
    return bool(EMAIL_REGEX.match(email_value))


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_template(path: str, fallback: str) -> str:
    if not path:
        return fallback
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_sent_set(path: str) -> set:
    if not os.path.exists(path):
        return set()
    data = load_json(path)
    if isinstance(data, list):
        return {normalize_email(x) for x in data if isinstance(x, str)}
    if isinstance(data, dict):
        entries = data.get("sent", [])
        return {normalize_email(x) for x in entries if isinstance(x, str)}
    return set()


def save_sent_set(path: str, sent_set: set) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "sent": sorted(list(sent_set)),
        "count": len(sent_set),
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)


def build_message(
    from_email: str,
    from_name: str,
    to_email: str,
    subject: str,
    text_body: str,
    html_body: str,
    service_id: str,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = from_email
    msg["X-Service-ID"] = service_id or "unknown"
    msg["X-Campaign"] = "hostinger-bulk-send"
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    return msg


def main() -> int:
    args = parse_args()

    smtp_host = os.getenv("SMTP_HOST", "smtp.hostinger.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER", "ionut@ionesculaw.ro")
    smtp_password = os.getenv("SMTP_PASSWORD", "")

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}")
        return 2

    try:
        payload = load_json(args.input)
    except Exception as exc:
        print(f"ERROR: Could not parse JSON: {exc}")
        return 2

    recipients_raw = payload.get("recipients", [])
    if not isinstance(recipients_raw, list):
        print("ERROR: JSON invalid. Campul 'recipients' trebuie sa fie lista.")
        return 2

    already_sent = load_sent_set(args.resume_file)
    text_template = load_template(args.text_template, DEFAULT_TEXT_TEMPLATE)
    html_template = load_template(args.html_template, DEFAULT_HTML_TEMPLATE)

    valid = []
    skipped_invalid = []
    skipped_duplicate = []
    skipped_already_sent = []
    seen = set()

    for rec in recipients_raw:
        if not isinstance(rec, dict):
            continue
        raw_email = str(rec.get("email", ""))
        email = normalize_email(raw_email)
        name = str(rec.get("name", "")).strip() or "Service Auto"
        service_id = str(rec.get("service_id", "")).strip()

        if not is_valid_email(email):
            skipped_invalid.append({"email": raw_email, "name": name, "reason": "invalid_email"})
            continue
        if email in seen:
            skipped_duplicate.append({"email": email, "name": name, "reason": "duplicate_in_input"})
            continue
        if email in already_sent:
            skipped_already_sent.append({"email": email, "name": name, "reason": "already_sent"})
            continue

        seen.add(email)
        valid.append({"email": email, "name": name, "service_id": service_id})

    if args.limit > 0:
        valid = valid[: args.limit]

    print(f"Input recipients: {len(recipients_raw)}")
    print(f"Valid recipients: {len(valid)}")
    print(f"Skipped invalid: {len(skipped_invalid)}")
    print(f"Skipped duplicates: {len(skipped_duplicate)}")
    print(f"Skipped already sent: {len(skipped_already_sent)}")
    print(f"SMTP target: {smtp_host}:{smtp_port} as {smtp_user}")
    print(f"Dry run: {args.dry_run}")

    if args.dry_run:
        return 0

    if not smtp_password:
        print("ERROR: SMTP_PASSWORD nu este setat in environment.")
        return 2

    if not valid:
        print("No recipients to send.")
        return 0

    sent_now = []
    failed = []

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=30) as smtp:
        smtp.login(smtp_user, smtp_password)
        for index, rec in enumerate(valid, start=1):
            msg = build_message(
                from_email=smtp_user,
                from_name=args.from_name,
                to_email=rec["email"],
                subject=args.subject,
                text_body=text_template,
                html_body=html_template,
                service_id=rec["service_id"],
            )
            try:
                smtp.send_message(msg)
                sent_now.append(
                    {
                        "email": rec["email"],
                        "name": rec["name"],
                        "service_id": rec["service_id"],
                        "status": "sent",
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                    }
                )
                print(f"[{index}/{len(valid)}] SENT {rec['email']}")
            except Exception as exc:
                failed.append(
                    {
                        "email": rec["email"],
                        "name": rec["name"],
                        "service_id": rec["service_id"],
                        "status": "failed",
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "error": str(exc),
                    }
                )
                print(f"[{index}/{len(valid)}] FAIL {rec['email']} -> {exc}")

            if index < len(valid) and args.delay > 0:
                time.sleep(args.delay)

    updated_sent = already_sent.union({x["email"] for x in sent_now})
    save_sent_set(args.resume_file, updated_sent)

    Path(args.results_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(args.results_dir) / f"email_results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    output = {
        "run_at": datetime.utcnow().isoformat() + "Z",
        "input_file": args.input,
        "subject": args.subject,
        "smtp_host": smtp_host,
        "smtp_user": smtp_user,
        "counts": {
            "input": len(recipients_raw),
            "valid": len(valid),
            "sent": len(sent_now),
            "failed": len(failed),
            "skipped_invalid": len(skipped_invalid),
            "skipped_duplicates": len(skipped_duplicate),
            "skipped_already_sent": len(skipped_already_sent),
        },
        "sent": sent_now,
        "failed": failed,
        "skipped_invalid": skipped_invalid,
        "skipped_duplicates": skipped_duplicate,
        "skipped_already_sent": skipped_already_sent,
    }
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)

    print(f"Done. Sent={len(sent_now)} Failed={len(failed)}")
    print(f"Results: {output_path}")
    print(f"Resume file: {args.resume_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
