#!/usr/bin/env python3
"""
Bridge local pentru dashboard:
- primește din webapp lista de service-uri selectate
- trimite email-urile prin Apple Mail (folosind trimite_emailuri_apple_mail.py)
- actualizează istoricul local și returnează rezultat JSON
"""

import argparse
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Tuple

from trimite_emailuri_apple_mail import (
    DEFAULT_HISTORY_PATH,
    DEFAULT_RESULTS_DIR,
    dedupe_and_filter,
    history_indexes,
    is_valid_email,
    load_history,
    normalize_email,
    now_iso,
    persist_result_log,
    send_bulk,
)

PROJECT_ROOT = Path(__file__).resolve().parent
SEND_LOCK = Lock()


def _resolve_path(value: str, default_relative: Path) -> Path:
    if value:
        p = Path(value).expanduser()
    else:
        p = default_relative
    if p.is_absolute():
        return p
    return (PROJECT_ROOT / p).resolve()


def _normalize_recipients(raw_recipients: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    valid: List[Dict[str, str]] = []
    invalid: List[Dict[str, str]] = []

    for row in raw_recipients:
        service_id = str((row or {}).get("service_id", "")).strip()
        name = str((row or {}).get("name", "")).strip() or "Service Auto"
        email_raw = str((row or {}).get("email", "")).strip()
        email = normalize_email(email_raw)

        if not is_valid_email(email):
            invalid.append(
                {
                    "service_id": service_id,
                    "name": name,
                    "email": email_raw,
                    "reason": "invalid_email",
                }
            )
            continue

        valid.append(
            {
                "service_id": service_id,
                "name": name,
                "email": email,
                "source_file": "webapp-direct-send",
            }
        )

    return valid, invalid


def _build_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload invalid: aștept un JSON object.")

    raw_recipients = payload.get("recipients", [])
    if not isinstance(raw_recipients, list):
        raise ValueError("Payload invalid: 'recipients' trebuie să fie listă.")
    if not raw_recipients:
        raise ValueError("Lista 'recipients' este goală.")

    delay = float(payload.get("delay", 1.0))
    if delay < 0:
        delay = 0.0

    dry_run = bool(payload.get("dry_run", False))
    force_resend = bool(payload.get("force_resend", False))

    history_path = _resolve_path(str(payload.get("history_path", "")), DEFAULT_HISTORY_PATH)
    results_dir = _resolve_path(str(payload.get("results_dir", "")), DEFAULT_RESULTS_DIR)

    candidates, invalid = _normalize_recipients(raw_recipients)

    history = load_history(history_path)
    sent_emails, sent_service_ids = history_indexes(history)
    to_send, skipped = dedupe_and_filter(
        candidates,
        sent_emails=sent_emails,
        sent_service_ids=sent_service_ids,
        force_resend=force_resend,
    )

    before_len = len(history.get("entries", []))
    send_result = send_bulk(
        recipients=to_send,
        delay_seconds=delay,
        dry_run=dry_run,
        history=history,
        history_path=history_path,
    )

    after_entries = history.get("entries", [])
    sent_entries = after_entries[before_len:]

    report = {
        "created_at": now_iso(),
        "mode": "dry-run" if dry_run else "send",
        "source": "webapp-local-bridge",
        "summary": {
            "loaded_candidates": len(candidates),
            "invalid": len(invalid),
            "skipped": len(skipped),
            "eligible": len(to_send),
            "sent": send_result["sent"],
            "failed": len(send_result["failed"]),
        },
        "invalid_entries": invalid,
        "skipped_entries": skipped,
        "failed_entries": send_result["failed"],
    }
    report_path = persist_result_log(results_dir, report)

    return {
        "ok": True,
        "created_at": now_iso(),
        "summary": report["summary"],
        "invalid_entries": invalid,
        "skipped_entries": skipped,
        "failed_entries": send_result["failed"],
        "sent_entries": sent_entries,
        "history_path": str(history_path),
        "report_path": str(report_path),
    }


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "LocalMailBridge/1.0"

    def _set_json_headers(self, status_code: int = 200) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def _write_json(self, data: Dict[str, Any], status_code: int = 200) -> None:
        self._set_json_headers(status_code)
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._set_json_headers(204)

    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/health"):
            self._write_json(
                {
                    "ok": True,
                    "busy": SEND_LOCK.locked(),
                    "timestamp": now_iso(),
                }
            )
            return

        self._write_json({"ok": False, "error": "Not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        if not self.path.startswith("/send-selected"):
            self._write_json({"ok": False, "error": "Not found"}, 404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json({"ok": False, "error": "JSON invalid."}, 400)
            return

        if not SEND_LOCK.acquire(blocking=False):
            self._write_json({"ok": False, "error": "Există deja o trimitere în curs."}, 409)
            return

        try:
            result = _build_report(payload)
            self._write_json(result, 200)
        except ValueError as exc:
            self._write_json({"ok": False, "error": str(exc)}, 400)
        except Exception as exc:  # pylint: disable=broad-except
            self._write_json({"ok": False, "error": f"Eroare internă: {exc}"}, 500)
        finally:
            SEND_LOCK.release()

    def log_message(self, fmt: str, *args: Any) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {self.address_string()} - {fmt % args}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local bridge pentru trimitere email din dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Host listen. Implicit: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8765, help="Port listen. Implicit: 8765")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), BridgeHandler)
    print(f"Local Mail Bridge rulează la http://{args.host}:{args.port}")
    print("Lasă acest proces deschis cât timp trimiți din webapp.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nOprire bridge.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
