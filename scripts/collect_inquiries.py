#!/usr/bin/env python3
"""LEMONICA sale landing — inquiry collector (watchdog for cron no_agent).

Polls the Farmer's Milk SMM mailbox for FormSubmit inquiries from the sale
landing, appends new ones to a CSV ledger and prints them to stdout (cron
delivers stdout to the origin chat). Silent when there is nothing new.
"""

import csv
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/Users/denysharbuzov/Documents/Limonika_Sale_Landing_2026-09-02")
LEDGER = BASE / "inquiries" / "Lemonica_Inquiries.csv"
STATE = BASE / "inquiries" / "processed_envelopes.json"


def run_json(args, timeout=120):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "command failed").strip()[-500:])
    return json.loads(result.stdout)


def load_state():
    if not STATE.exists():
        return set()
    return {str(x) for x in json.loads(STATE.read_text(encoding="utf-8"))}


def save_state(processed):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(processed), ensure_ascii=False, indent=1), encoding="utf-8")


def extract(pattern, text):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else ""


PHONE_RE = r"Phone\s*/\s*WhatsApp[:\s]+([^\n\r|—]*[0-9+][^\n\r|]*)"


def main():
    envelopes = run_json([
        "himalaya", "-o", "json", "envelope", "list",
        "subject LEMONICA",
    ])
    if isinstance(envelopes, dict):
        envelopes = envelopes.get("envelopes", [])
    processed = load_state()
    fresh = []
    for env in envelopes:
        env_id = str(env.get("id") or env.get("uid") or "")
        subject = str(env.get("subject") or "")
        sender = str((env.get("from") or {}).get("addr") or (env.get("from") or {}).get("name") or "")
        if "formsubmit" not in sender.lower():
            continue
        if env_id and env_id in processed:
            continue
        if env_id:
            processed.add(env_id)
        date = str(env.get("date") or "")
        name = subject.split("—", 1)[1].strip() if "—" in subject else ""

        body = ""
        try:
            msg = run_json(["himalaya", "-o", "json", "message", "read", env_id])
            text = msg if isinstance(msg, str) else json.dumps(msg, ensure_ascii=False)
            body = text
        except Exception:
            pass

        email = extract(r"Email[:\s]+([^\s|]+@[^\s|]+)", body)
        phone = extract(PHONE_RE, body)
        message = extract(r"Message[:\s]+(.+?)(?:\n\s*\n|Submitted)", body)[:400]

        if not name and not email:
            save_state(processed)
            continue

        row = {
            "date_utc": date,
            "name": name,
            "email": email,
            "phone": phone,
            "message": re.sub(r"\s+", " ", message).strip(),
            "envelope_id": env_id,
        }
        fresh.append(row)

    if not fresh:
        return

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    new_file = not LEDGER.exists()
    with LEDGER.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date_utc", "name", "email", "phone", "message", "envelope_id"])
        if new_file:
            writer.writeheader()
        writer.writerows(fresh)
    save_state(processed)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"🍋 LEMONICA: {len(fresh)} new inquiry(ies) | ledger: inquiries/Lemonica_Inquiries.csv | {now}")
    for r in fresh:
        print(f"— {r['name']} · {r['email']} · {r['phone'] or 'no phone'}")
        if r["message"]:
            print(f"  «{r['message'][:160]}»")


if __name__ == "__main__":
    main()
