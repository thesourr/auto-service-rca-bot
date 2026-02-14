#!/usr/bin/env python3
"""
Script simplu pentru trimitere email-uri prin Apple Mail (macOS).
Folosește contul deja configurat în aplicația Mail.

Funcții:
- trimite către adrese directe (--to)
- trimite din unul sau mai multe fișiere JSON exportate din dashboard (--input)
- trimite setul de test (--test)
- păstrează istoric local pentru a evita dublurile
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

SENDER = "ionut@ionesculaw.ro"
SUBJECT = "Propunere colaborare profesională"
DEFAULT_HISTORY_PATH = Path("data/sent_emails_history.json")
DEFAULT_RESULTS_DIR = Path("data")

EMAIL_BODY = """Stimată Doamnă / Stimate Domnule,


Numele meu este Ionescu Virgiliu-Ionuț și sunt avocat în Baroul București, cu experiență în recuperarea sumelor de bani datorate de societățile de asigurare în dosarele de daună RCA.

Vă contactez pentru a vă propune o colaborare profesională prin care să sprijin service-ul dumneavoastră în recuperarea integrală a sumelor aferente reparațiilor auto, în situațiile în care asigurătorii RCA refuză plata, diminuează nejustificat despăgubirile sau tergiversează soluționarea dosarelor de daună.


În cadrul colaborării, pot asigura:

analizarea dosarelor de daună și a documentației aferente;

formularea notificărilor și a demersurilor prealabile;

reprezentare în fața instanțelor de judecată;

recuperarea penalităților și a dobânzilor legale, acolo unde este cazul.


Obiectivul este protejarea intereselor service-ului și maximizarea recuperării sumelor cuvenite, fără a afecta relația cu clienții dumneavoastră.

Sunt disponibil pentru o discuție telefonică sau o întâlnire (online sau fizic) în vederea stabilirii detaliilor unei eventuale colaborări. Caz în care îmi puteți răspunde la acest email cu un număr de telefon la care vă pot contacta.

Vă mulțumesc pentru timpul acordat și aștept cu interes un răspuns din partea dumneavoastră.


Cu aleasă considerație,
Virgiliu-Ionuț IONESCU
Managing Partner
ionesculaw.ro"""

TEST_RECIPIENTS = [
    "ionescuionut18@gmail.com",
    "thesourgta@gmail.com",
    "ionescuionut20@gmail.com",
]

# E suficient de strict pentru a elimina adrese generate din artefacte JS/CSS
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$")
DISALLOWED_TLDS = {"png", "jpg", "jpeg", "gif", "svg", "webp", "css", "js", "map", "json", "ico", "woff", "woff2"}
PLACEHOLDER_DOMAINS = {"example.com", "exemplu.ro", "domeniu.com", "yoursite.com"}

APPLESCRIPT_SEND = r'''
on run argv
    set subjectLine to item 1 of argv
    set bodyText to item 2 of argv
    set senderAddress to item 3 of argv
    set recipientAddress to item 4 of argv

    tell application "Mail"
        set newMessage to make new outgoing message with properties {subject:subjectLine, content:bodyText, visible:false}
        tell newMessage
            set sender to senderAddress
            make new to recipient at end of to recipients with properties {address:recipientAddress}
            send
        end tell
    end tell
end run
'''


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_email(value: str) -> str:
    email = (value or "").strip().strip("<>").strip()
    while email and email[-1] in ".,;:":
        email = email[:-1]
    return email.lower()


def is_valid_email(value: str) -> bool:
    email = normalize_email(value)
    if not email or ".." in email:
        return False
    if not EMAIL_REGEX.fullmatch(email):
        return False

    domain = email.split("@", 1)[1]
    tld = domain.rsplit(".", 1)[-1]
    if domain in PLACEHOLDER_DOMAINS:
        return False
    if tld in DISALLOWED_TLDS:
        return False
    return True


def send_email(recipient: str, subject: str = SUBJECT, body: str = EMAIL_BODY, sender: str = SENDER) -> None:
    subprocess.run(
        ["osascript", "-e", APPLESCRIPT_SEND, subject, body, sender, recipient],
        check=True,
        capture_output=True,
        text=True,
    )


def normalize_recipients(raw: Iterable[str]) -> List[str]:
    unique: List[str] = []
    seen: Set[str] = set()
    for item in raw:
        email = normalize_email(item)
        if not email:
            continue
        if not is_valid_email(email):
            raise ValueError(f"Adresă invalidă: {item}")
        if email not in seen:
            seen.add(email)
            unique.append(email)
    return unique


def load_history(history_path: Path) -> Dict:
    if not history_path.exists():
        return {"version": 1, "sender": SENDER, "updated_at": None, "entries": []}

    with history_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries")
    if not isinstance(entries, list):
        data["entries"] = []
    return data


def save_history(history_path: Path, history: Dict) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history["updated_at"] = now_iso()
    with history_path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def history_indexes(history: Dict) -> Tuple[Set[str], Set[str]]:
    emails: Set[str] = set()
    service_ids: Set[str] = set()

    for entry in history.get("entries", []):
        email = normalize_email(entry.get("email", ""))
        service_id = (entry.get("service_id") or "").strip()
        if email:
            emails.add(email)
        if service_id:
            service_ids.add(service_id)

    return emails, service_ids


def load_recipients_from_files(paths: List[Path]) -> Tuple[List[Dict], List[Dict]]:
    loaded: List[Dict] = []
    invalid: List[Dict] = []

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Fișierul nu există: {path}")

        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        recipients = payload.get("recipients")
        if not isinstance(recipients, list):
            raise ValueError(f"Fișier invalid (lipsește lista recipients): {path}")

        for row in recipients:
            service_id = str((row or {}).get("service_id", "")).strip()
            email_raw = str((row or {}).get("email", "")).strip()
            name = str((row or {}).get("name", "")).strip() or "Service Auto"
            email = normalize_email(email_raw)

            if not is_valid_email(email):
                invalid.append(
                    {
                        "source_file": str(path),
                        "service_id": service_id,
                        "name": name,
                        "email": email_raw,
                        "reason": "invalid_email",
                    }
                )
                continue

            loaded.append(
                {
                    "service_id": service_id,
                    "email": email,
                    "name": name,
                    "source_file": str(path),
                }
            )

    return loaded, invalid


def dedupe_and_filter(
    recipients: List[Dict],
    sent_emails: Set[str],
    sent_service_ids: Set[str],
    force_resend: bool,
) -> Tuple[List[Dict], List[Dict]]:
    ready: List[Dict] = []
    skipped: List[Dict] = []
    batch_seen_emails: Set[str] = set()

    for row in recipients:
        email = normalize_email(row.get("email", ""))
        service_id = (row.get("service_id") or "").strip()

        if email in batch_seen_emails:
            skipped.append({**row, "reason": "duplicate_in_input"})
            continue
        batch_seen_emails.add(email)

        if not force_resend:
            already_sent = email in sent_emails
            if service_id:
                already_sent = already_sent or service_id in sent_service_ids
            if already_sent:
                skipped.append({**row, "reason": "already_sent"})
                continue

        ready.append(row)

    return ready, skipped


def persist_result_log(results_dir: Path, report: Dict) -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    output_path = results_dir / f"send_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return output_path


def send_bulk(
    recipients: List[Dict],
    delay_seconds: float,
    dry_run: bool,
    history: Dict,
    history_path: Path,
) -> Dict:
    total = len(recipients)
    sent_count = 0
    failed: List[Dict] = []

    if total == 0:
        print("Nu există destinatari eligibili pentru trimitere.")
        return {"sent": 0, "failed": []}

    print(f"Se procesează {total} email-uri de pe {SENDER}...")

    for idx, recipient in enumerate(recipients, start=1):
        email = recipient["email"]
        name = recipient.get("name", "Service Auto")

        if dry_run:
            print(f"[{idx}/{total}] [DRY-RUN] Ar trimite către: {email} ({name})")
            continue

        try:
            send_email(email)
            sent_count += 1
            print(f"[{idx}/{total}] Trimis: {email} ({name})")

            history.setdefault("entries", []).append(
                {
                    "service_id": recipient.get("service_id", ""),
                    "email": email,
                    "name": name,
                    "source_file": recipient.get("source_file", ""),
                    "sent_at": now_iso(),
                    "subject": SUBJECT,
                    "sender": SENDER,
                }
            )
            save_history(history_path, history)

        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            print(f"[{idx}/{total}] EROARE la {email}: {stderr or exc}")
            failed.append(
                {
                    "service_id": recipient.get("service_id", ""),
                    "email": email,
                    "name": name,
                    "source_file": recipient.get("source_file", ""),
                    "error": stderr or str(exc),
                }
            )

        if idx < total and delay_seconds > 0:
            time.sleep(delay_seconds)

    print("Gata.")
    return {"sent": sent_count, "failed": failed}


def send_test() -> List[Dict]:
    recipients: List[Dict] = []
    for idx, email in enumerate(TEST_RECIPIENTS, start=1):
        recipients.append(
            {
                "service_id": f"test-{idx}",
                "email": normalize_email(email),
                "name": "Test Recipient",
                "source_file": "--test",
            }
        )
    return recipients


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trimite email-uri prin Apple Mail (cont local configurat)."
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Trimite email-ul către cele 3 adrese de test predefinite.",
    )
    parser.add_argument(
        "--to",
        nargs="+",
        help="Listează adresele de email către care trimiți (separate prin spațiu).",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        help="Fișiere JSON exportate din dashboard (ex: email_recipients-2.json).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Pauză (secunde) între email-uri. Implicit: 1.0",
    )
    parser.add_argument(
        "--history",
        default=str(DEFAULT_HISTORY_PATH),
        help=f"Fișierul de istoric trimiteri. Implicit: {DEFAULT_HISTORY_PATH}",
    )
    parser.add_argument(
        "--results-dir",
        default=str(DEFAULT_RESULTS_DIR),
        help=f"Folderul unde se salvează raportul de rulare. Implicit: {DEFAULT_RESULTS_DIR}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nu trimite efectiv email-uri, doar simulează și afișează ce s-ar trimite.",
    )
    parser.add_argument(
        "--force-resend",
        action="store_true",
        help="Ignoră istoricul și retrimite chiar dacă adresa/service-ul există deja.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        history_path = Path(args.history)
        results_dir = Path(args.results_dir)

        history = load_history(history_path)
        sent_emails, sent_service_ids = history_indexes(history)

        invalid_from_files: List[Dict] = []

        if args.test:
            candidates = send_test()
        elif args.input:
            input_paths = [Path(p).expanduser() for p in args.input]
            candidates, invalid_from_files = load_recipients_from_files(input_paths)
        elif args.to:
            emails = normalize_recipients(args.to)
            candidates = [
                {
                    "service_id": "",
                    "email": email,
                    "name": "Manual recipient",
                    "source_file": "--to",
                }
                for email in emails
            ]
        else:
            print("Folosește --test, --input sau --to.")
            return 1

        to_send, skipped = dedupe_and_filter(
            candidates,
            sent_emails=sent_emails,
            sent_service_ids=sent_service_ids,
            force_resend=args.force_resend,
        )

        print("=" * 70)
        print("Rezumat pregătire listă")
        print("=" * 70)
        print(f"Candidati încărcați: {len(candidates)}")
        print(f"Invalidi eliminați: {len(invalid_from_files)}")
        print(f"Skip duplicate/trimise deja: {len(skipped)}")
        print(f"De trimis acum: {len(to_send)}")

        send_result = send_bulk(
            recipients=to_send,
            delay_seconds=max(0.0, args.delay),
            dry_run=args.dry_run,
            history=history,
            history_path=history_path,
        )

        report = {
            "created_at": now_iso(),
            "mode": "dry-run" if args.dry_run else "send",
            "sender": SENDER,
            "subject": SUBJECT,
            "source": {
                "test": args.test,
                "input_files": args.input or [],
                "manual_to": args.to or [],
            },
            "summary": {
                "loaded_candidates": len(candidates),
                "invalid_filtered": len(invalid_from_files),
                "skipped": len(skipped),
                "eligible": len(to_send),
                "sent": send_result["sent"],
                "failed": len(send_result["failed"]),
            },
            "invalid_entries": invalid_from_files,
            "skipped_entries": skipped,
            "failed_entries": send_result["failed"],
        }

        report_path = persist_result_log(results_dir, report)
        print(f"Raport salvat: {report_path}")
        print(f"Istoric trimiteri: {history_path}")

        return 0

    except ValueError as exc:
        print(f"Eroare date: {exc}")
        return 1
    except FileNotFoundError as exc:
        msg = str(exc)
        if "osascript" in msg:
            print("Comanda 'osascript' nu a fost găsită. Scriptul trebuie rulat pe macOS.")
        else:
            print(msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
